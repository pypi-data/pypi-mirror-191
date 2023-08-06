"""Module for parsing CCSDS packets using packet definitions"""
# Standard
import datetime as dt
import time
import warnings
from collections import namedtuple
import logging
from typing import Tuple
# Installed
import bitstring
# Local
from lasp_packets import xtcedef, csvdef

logger = logging.getLogger(__name__)


CcsdsPacketHeaderElement = namedtuple('CcsdsPacketHeaderElement', ['name', 'format_string'])

CCSDS_HEADER_DEFINITION = [
    CcsdsPacketHeaderElement('VERSION', 'uint:3'),
    CcsdsPacketHeaderElement('TYPE', 'uint:1'),
    CcsdsPacketHeaderElement('SEC_HDR_FLG', 'uint:1'),
    CcsdsPacketHeaderElement('PKT_APID', 'uint:11'),
    CcsdsPacketHeaderElement('SEQ_FLGS', 'uint:2'),
    CcsdsPacketHeaderElement('SRC_SEQ_CTR', 'uint:14'),
    CcsdsPacketHeaderElement('PKT_LEN', 'uint:16')
]

CCSDS_HEADER_LENGTH_BITS = 48

Packet = namedtuple('Packet', ['header', 'data'])


class ParsedDataItem(xtcedef.AttrComparable):
    """Representation of a parsed parameter"""

    def __init__(self, name: str, raw_value: any, unit: str = None, derived_value: float or str = None):
        """Constructor

        Parameters
        ----------
        name : str
            Parameter name
        unit : str
            Parameter units
        raw_value : any
            Raw representation of the parsed value. May be lots of different types but most often an integer
        derived_value : float or str
            May be a calibrated value or an enum lookup
        """
        if name is None or raw_value is None:
            raise ValueError("Invalid ParsedDataItem. Must define name and raw_value.")
        self.name = name
        self.raw_value = raw_value
        self.unit = unit
        self.derived_value = derived_value

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"{self.name}, raw={self.raw_value}, derived={self.derived_value}, unit={self.unit}"
                f")")


class UnrecognizedPacketTypeError(Exception):
    """Error raised when we can't figure out which kind of packet we are dealing with based on the header"""
    def __init__(self, *args, partial_data: dict = None):
        """
        Parameters
        ----------
        partial_data : dict, Optional
            Data parsed so far (for debugging at higher levels)
        """
        super().__init__(*args)
        self.partial_data = partial_data


class PacketParser:
    """Class for parsing CCSDS packets"""

    def __init__(self,
                 packet_definition: xtcedef.XtcePacketDefinition or csvdef.CsvPacketDefinition,
                 word_size: int = None,
                 header_name_mappings: dict = None):
        """Constructor

        Parameters
        ----------
        packet_definition: xtcedef.XtcePacketDefinition or csvdef.CsvPacketDefinition
            The packet definition object to use for parsing incoming data.
        word_size: int, Optional
            Number of bits per word. If set, binary parameters are assumed to end on a word boundary and any unused bits
            at the end of each binary parameter are skipped. Default is no word boundary enforcement. Typical usecase
            is 32bit words.
        header_name_mappings : dict, Optional
            If the XTCE definition uses different header item names than VERSION, TYPE, SEC_HDR_FLG, PKT_APID,
            SEQ_FLGS, SRC_SEQ_CTR, and PKT_LEN, you can pass in a dict mapping these to other names for purposes of
            restrictions or logical operations during parsing.
        """
        self.packet_definition = packet_definition
        self.word_size = word_size
        self.header_name_mappings = header_name_mappings

    @staticmethod
    def _parse_header(packet_data: bitstring.ConstBitStream,
                      start_position: int = None,
                      reset_cursor: bool = False,
                      header_name_mappings: dict = None) -> dict:
        """Parses the CCSDS standard header.

        Parameters
        ----------
        packet_data : bitstring.ConstBitStream
            Binary data stream of packet data.
        start_position : int
            Position from which to start parsing. If not provided, will start whenever the cursor currently is.
        reset_cursor : bool
            If True, upon parsing the header data, reset the cursor to the original position in the stream.
            This still applies even if start_position is specified. start_position will be used only for parsing the
            header and then the cursor will be returned to the location it was at before this function was called.
        header_name_mappings : dict, Optional
            If set, used to rename the parsed header values to the custom names.

        Returns
        -------
        header : dict
            Dictionary of header items.
        """
        # TODO: Remove this. Why is this useful?
        def _rename(name: str):
            """Renames header items to custom names if specified"""
            if header_name_mappings and name in header_name_mappings:
                return header_name_mappings[name]
            return name

        original_cursor_position = packet_data.pos

        if start_position:
            packet_data.pos = start_position

        header = {
            _rename(item.name): ParsedDataItem(name=_rename(item.name), unit=None,
                                               raw_value=packet_data.read(item.format_string))
            for item in CCSDS_HEADER_DEFINITION
        }

        if reset_cursor:
            packet_data.pos = original_cursor_position

        return header

    @staticmethod
    def _total_packet_bits_from_pkt_len(pkt_len: int):
        """Calculate the total length of a CCSDS packet in bits based on the PKT_LEN field in its header.

        Parameters
        ----------
        pkt_len : int
            PKT_LEN value from CCSDS header

        Returns
        -------
        : int
            Length, in bits of the packet
        """
        # 4.1.3.5.3 The length count C shall be expressed as:
        #   C = (Total Number of Octets in the Packet Data Field) – 1
        # We also just re-parsed the CCSDS header though as well, so that's an additional 6 octets
        return 8 * (pkt_len + 1 + 6)

    def _determine_packet_by_restrictions(self, parsed_header: dict) -> Tuple[str, list]:
        """Examines a dictionary representation of a CCSDS header and determines which packet type applies.
        This packet type must be unique. If the header data satisfies the restrictions for more than one packet
        type definition, an exception is raised.

        Parameters
        ----------
        parsed_header : dict
            Pre-parsed header data in dictionary form for evaluating restriction criteria.
            NOTE: Restriction criteria can ONLY be evaluated against header items. There is no reasonable way to
            start parsing all the BaseContainer inheritance restrictions without assuming that all restrictions will
            be based on header items, which can be parsed ahead of time due to the consistent nature of a CCSDS header.

        Returns
        -------
        : str
            Name of packet definition.
        : list
            A list of Parameter objects
        """
        flattened_containers = self.packet_definition.flattened_containers
        meets_requirements = []
        for container_name, flattened_container in flattened_containers.items():
            try:
                checks = [
                    criterion.evaluate(parsed_header)
                    for criterion in flattened_container.restrictions
                ]
            except AttributeError as err:
                raise ValueError("Hitherto unparsed parameter name found in restriction criteria for container "
                                 f"{container_name}. Because we can't parse packet data until we know the type, "
                                 "only higher up parameters (e.g. APID) are permitted as container "
                                 "restriction criteria.") from err

            if all(checks):
                meets_requirements.append(container_name)

        if len(meets_requirements) == 1:
            name = meets_requirements.pop()
            return name, flattened_containers[name].entry_list

        if len(meets_requirements) > 1:
            raise UnrecognizedPacketTypeError(
                "Found more than one possible packet definition based on restriction criteria. "
                f"{meets_requirements}", partial_data=parsed_header)

        if len(meets_requirements) < 1:
            raise UnrecognizedPacketTypeError(
                "Header does not allow any packet definitions based on restriction criteria. "
                f"Unable to choose a packet type to parse. "
                "Note: Restricting container inheritance based on non-header data items is not possible in a "
                "general way and is not supported by this package.", partial_data=parsed_header)

    @staticmethod
    def parse_packet(packet_data: bitstring.ConstBitStream, 
                     containers: dict, 
                     root_container_name: str = "CCSDSPacket", 
                     **parse_value_kwargs) -> Packet:
        """Parse binary packet data according to the self.packet_definition object

        Parameters
        ----------
        packet_data : bitstring.BitString
            Binary packet data to parse into Packets
        containers : dict
            Dictionary of named containers, including their inheritance information.
        root_container_name : str, Optional
            Default is CCSDSPacket. Any root container may be specified.

        Returns
        -------
        Packet
            A Packet object container header and data attributes.
        """

        def _parse_parameter(p: xtcedef.Parameter):
            logger.debug(f'Parsing {p} of type {p.parameter_type}')
            parsed_value, derived_value = p.parameter_type.parse_value(
                packet_data, parsed_data=parsed_items, **parse_value_kwargs)

            logger.debug(f"Parsed value: {parsed_value}")
            parsed_items[p.name] = ParsedDataItem(
                name=p.name,
                unit=p.parameter_type.unit,
                raw_value=parsed_value,
                derived_value=derived_value
            )

        def _parse_sequence_container(sc: xtcedef.SequenceContainer):
            for e in sc.entry_list:
                if isinstance(e, xtcedef.SequenceContainer):
                    _parse_sequence_container(e)
                else:
                    _parse_parameter(e)

        parsed_items = {}
        current_container: xtcedef.SequenceContainer = containers[root_container_name]
        while True:
            for entry in current_container.entry_list:
                if isinstance(entry, xtcedef.Parameter):
                    _parse_parameter(entry)
                elif isinstance(entry, xtcedef.SequenceContainer):
                    _parse_sequence_container(entry)

            valid_inheritors = []
            for inheritor_name in current_container.inheritors:
                if all([rc.evaluate(parsed_items) for rc in containers[inheritor_name].restriction_criteria]):
                    valid_inheritors.append(inheritor_name)

            if len(valid_inheritors) == 1:
                # Set the unique valid inheritor as the next current_container
                current_container = containers[valid_inheritors[0]]
                continue
            elif len(valid_inheritors) == 0:
                if current_container.abstract is True:
                    raise UnrecognizedPacketTypeError(
                        f"Detected an abstract container with no valid inheritors by restriction criteria. This might "
                        f"mean this packet type is not accounted for in the provided packet definition. "
                        f"APID={parsed_items['PKT_APID'].raw_value}.",
                        partial_data=parsed_items)
                break

            raise UnrecognizedPacketTypeError(
                f"Multiple valid inheritors, {valid_inheritors} are possible for {current_container}.",
                partial_data=parsed_items)
        header = dict(list(parsed_items.items())[:7])
        user_data = dict(list(parsed_items.items())[7:])
        return Packet(header, user_data)

    @staticmethod
    def legacy_parse_packet(packet_data: bitstring.ConstBitStream, entry_list: list, **parse_value_kwargs) -> Packet:
        """Parse binary packet data according to the self.packet_definition object

        Parameters
        ----------
        packet_data : bitstring.BitString
            Binary packet data to parse into Packets
        entry_list : list
            List of Parameter objects

        Returns
        -------
        Packet
            A Packet object container header and data attributes.
        """
        header = {}
        for parameter in entry_list[0:7]:
            # logger.debug(f'Parsing header item {parameter}')
            parsed_value, _ = parameter.parameter_type.parse_value(packet_data, header)

            header[parameter.name] = ParsedDataItem(
                name=parameter.name,
                unit=parameter.parameter_type.unit,
                raw_value=parsed_value
            )

        user_data = {}
        for parameter in entry_list[7:]:
            logger.debug(f'Parsing {parameter} of type {parameter.parameter_type}')
            combined_parsed_data = dict(**header)
            combined_parsed_data.update(user_data)
            parsed_value, derived_value = parameter.parameter_type.parse_value(
                packet_data, parsed_data=combined_parsed_data, **parse_value_kwargs)

            logger.debug(f"Parsed value: {parsed_value}")
            user_data[parameter.name] = ParsedDataItem(
                name=parameter.name,
                unit=parameter.parameter_type.unit,
                raw_value=parsed_value,
                derived_value=derived_value
            )

        return Packet(header=header, data=user_data)


    def generator(self,
                  binary_data: bitstring.ConstBitStream,
                  parse_bad_pkts: bool = True,
                  skip_header_bits: int = 0,
                  root_container_name="CCSDSPacket",
                  ccsds_headers_only: bool = False,
                  yield_unrecognized_packet_errors: bool = False,
                  show_progress: bool = False):
        """Create and return a Packet generator. Creating a generator object to return allows the user to create
        many generators from a single Parser and reduces memory usage.

        Parameters
        ----------
        binary_data : bitstring.ConstBitStream
            Binary data to parse into Packets.
        parse_bad_pkts : bool, Optional
            Default True.
            If True, when the generator encounters a packet with an incorrect length it will still yield the packet
            (the data will likely be invalid). If False, the generator will still write a debug log message but will
            otherwise silently skip the bad packet.
        skip_header_bits : int, Optional
            If provided, the parser skips this many bits at the beginning of every packet. This allows dynamic stripping
            of additional header data that may be prepended to packets.
        root_container_name : str, Optional
            The name of the root level (lowest level of container inheritance) SequenceContainer. This SequenceContainer
            is assumed to be inherited by every possible packet structure in the XTCE document and is the starting
            point for parsing. Default is 'CCSDSPacket'.
        ccsds_headers_only : bool, Optional
            If True, only parses the packet headers (does not use the provided packet definition).
        yield_unrecognized_packet_errors : bool, Optional
            If False, UnrecognizedPacketTypeErrors are caught silently and parsing continues to the next packet.
            If True, the generator will yield an UnrecognizedPacketTypeError in the event of an unrecognized
            packet. Note: These exceptions are not raised by default but are instead returned so that the generator
            can continue. You can raise the exceptions if desired. Leave this as False unless you need to examine the
            partial data from unrecognized packets.
        show_progress : bool, Optional
            If True, prints a status bar.

        Yields
        -------
        : Packet or UnrecognizedPacketTypeError
            Generator yields Packet objects containing the parsed packet data for each subsequent packet.
        """
        def progressbar(current_value, total_value, progress_char, end='\r'):
            bar_length=20
            percentage = int((current_value / total_value) * 100)  # Percent Completed Calculation
            progress = int((bar_length * current_value) / total_value)  # Progress Done Calculation
            loadbar = "Progress: [{:{len}}]{}%".format(progress * progress_char, percentage,
                                                       len=bar_length)  # Progress Bar String
            print(loadbar, end=end)

        start_time = time.time_ns()
        n_packets = 0
        total_length = len(binary_data)
        while binary_data.pos < total_length:
            if show_progress is True:
                progressbar(binary_data.pos, total_length, progress_char="=")


            if skip_header_bits:
                binary_data.pos += skip_header_bits

            # Parse the header but leave the cursor in the original position because the header is defined
            #   in the overall packet definition as well. We only parse the header here, so we can determine the
            #   packet definition type (usually by APID, VERSION, and TYPE but potentially based on
            #   any header data).
            packet_starting_position = binary_data.pos
            logger.debug(f"Parsing packet starting at {packet_starting_position}. Total length is {total_length}.")
            header = self._parse_header(binary_data, reset_cursor=True)
            n_packets += 1  # Consider it a counted packet once we've parsed the header
            specified_packet_data_length = self._total_packet_bits_from_pkt_len(header['PKT_LEN'].raw_value)
            if ccsds_headers_only is True:
                binary_data.pos += specified_packet_data_length
                yield Packet(header=header, data=None)
                continue

            logger.debug(
                f"Packet header: "
                f"{' '.join([str(parsed_param) for param_name, parsed_param in header.items()])}")

            try:
                if isinstance(self.packet_definition, xtcedef.XtcePacketDefinition):
                    packet = self.parse_packet(binary_data,
                                               self.packet_definition.named_containers,
                                               root_container_name=root_container_name,
                                               word_size=self.word_size)
                else:
                    packet_def_name, parameter_list = self._determine_packet_by_restrictions(header)
                    packet = self.legacy_parse_packet(binary_data, parameter_list, word_size=self.word_size)

            except UnrecognizedPacketTypeError as e:
                # Regardless of whether we handle it, we do want to move the cursor to the next packet
                binary_data.pos = packet_starting_position + specified_packet_data_length
                logger.debug(f"Unrecognized error on packet with APID {header['PKT_APID'].raw_value}'")
                if yield_unrecognized_packet_errors is True:
                    # Yield the caught exception without raising it (raising ends generator)
                    yield e
                    continue
                else:
                    # Silently continue to next packet
                    continue

            if packet.header['PKT_LEN'].raw_value != header['PKT_LEN'].raw_value:
                raise ValueError(f"Hardcoded header parsing found a different packet length "
                                 f"{header['PKT_LEN'].raw_value} than the definition-based parsing found "
                                 f"{packet.header['PKT_LEN'].raw_value}. This might be because the CCSDS header is "
                                 f"incorrectly represented in your packet definition document.")

            actual_length_parsed = binary_data.pos - packet_starting_position

            if actual_length_parsed != specified_packet_data_length:
                logger.warning(f"Parsed packet length starting at bit position: {binary_data.pos} "
                               f"({actual_length_parsed}b) did not match "
                               f"length specified in header ({specified_packet_data_length}b). "
                               f"Updating bit string position to correct position "
                               "indicated by CCSDS header.")
                binary_data.pos += specified_packet_data_length - actual_length_parsed
                if not parse_bad_pkts:
                    logger.warning("Skipping bad packet")
                    continue

            yield packet
        end_time = time.time_ns()
        elapsed_ns = end_time - start_time
        delta = dt.timedelta(microseconds=elapsed_ns / 1000)
        pps = int(n_packets * 1E9 / elapsed_ns)
        progressbar(binary_data.pos, total_length, progress_char="=", end=f" [Elapsed: {delta}, {pps} pkts/s]\n")
