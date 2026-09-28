from enum import IntEnum, auto
from modules.pymmh3 import hash_wide
import struct
import io

class Axis(IntEnum):
    X = 0
    Y = auto()
    Z = auto()
    W = auto()

class Transformation(IntEnum):
    Translation = 0
    Roatation = auto()
    Scale = auto()
    Blendshape = auto()
    UnkCtrl_4 = auto()
    UnkCtrl_5 = auto()
    Material_Color = auto()
    Material_4D = auto()
    Material_3D = auto()
    Material_2D = auto()
    Scalar = auto()
    Unknown_12 = auto()
    UnkRotation_13 = auto()
    UnkRotation_14 = auto()
    UnkRotation_15 = auto()
    UnkRotation_16 = auto()

class Updatetiming(IntEnum):
    MotionBegin = 0
    MotionEnd = auto()
    ConstraintBegin = auto()
    ConstraintEnd = auto()
    Last = auto()
    ByBehavior = auto()

class Transformation_Src(IntEnum):
    Translation = 0
    Rotation_1 = auto()
    Rotation_2 = auto()
    Rotation_3 = auto()
    UnkCtrl_4 = auto()

class SectionType(IntEnum):
    Transformation = 0
    RotationExpressions = auto()
    SkinConstraints = auto()
    Aim = auto()
    MaterialConstraints = auto()
    JointExportGraph = auto()

class EntryFlag(IntEnum):
    Constraint = auto()
    Source = auto()
    Name = auto()
    Dependency = auto()
    DependencyHash = auto()
    HashTable = auto()
    SectionType = auto()

def readname(Name_offset, file):
    current_offset = file.tell()
    file.seek(int(Name_offset, 16), 0)
    collected_bytes = bytearray()
    final_data = ''

    while True:
        chunk = file.read(16)
        if not chunk:
            break
        collected_bytes.extend(chunk)

        end_index = collected_bytes.find(b"\x00\x00\x00")
        if end_index != -1:
            final_data = collected_bytes[:end_index+1]
            break
    file.seek(current_offset, 0)
    return final_data.decode('utf-16le')

class jcns_class:

    class Header_class:
        _schema = [
            ("Version", 4),
            ("Signature", 4, str),
            ("Unknown00", 8),
            ("InfoEntry", 8),
            ("Unknown01", 8),
            ("JCNSEntry", 8),
            ("Unknown02", 8),
            ("Unknown03", 8),
            ("Unknown04", 8),
            ("DataEntry", 8),
            ("Unknown05", 8),
            ("ConeDriverTableEntry", 8, hex, None, EntryFlag.Constraint),
            ("ConstraintInfoEntry", 8, hex, None, EntryFlag.Constraint),
            ("ObjectSettingEntry", 8, hex, None, EntryFlag.SectionType),
            ("RotExpressionInfoEntry", 8, hex),
            ("RotExpressionMapEntry", 8, hex),
            ("RotExpressionSourceHashIndicesEntry", 8, hex),
            ("RotExpressionHashIndicesEntry", 8, hex),
            ("SkinConstraintTableEntry", 8, hex),
            ("SkinConstraintSourceTableEntry", 8, hex),
            ("AimConstraintTableEntry", 8, hex),
            ("MaterialConstraintInfoEntry", 8, hex),
            ("JointExportGraphInfoEntry", 8, hex),
            ("SectionTableEntry", 8, hex, None, EntryFlag.SectionType),
            ("DependencyTableEntry", 8, hex, None, EntryFlag.Dependency),
            ("HashTableEntry", 8, hex, None, EntryFlag.HashTable),
            ("SkinConstraintHashTableEntry", 8, hex),
            ("HashTableItemCount", 4),
            ("ConeDriverCount", 2),
            ("ConstraintCount", 2),
            ("DependencyCount", 2),
            ("ObjectSettingCount", 2),
            ("RotExpressionInfoCount", 2),
            ("RotExpressionMapCount", 2),
            ("SkinConstraintCount", 2),
            ("SkinConstraintHashTableItemCount", 2),
            ("SkinConstraintSourceCount", 2),
            ("AimConstraintCount", 2),
            ("MaterialConstraintInfoCount", 2),
            ("SectionCount", 1),
            ("Padding", 5, list, 1)
        ]

        def __init__(self):
            for item in self._schema:
                if len(item) > 2:
                    match item[2]:
                        case cls if cls is list:
                            setattr(self, item[0], [0] * (item[1] // item[3]))
                        case cls if cls in (str, hex):
                            setattr(self, item[0], '0')
                else:
                    setattr(self, item[0], 0)

            self.Version   = 102
            self.Signature = 'jcns'
            self.InfoEntry = 48
            self.JCNSEntry = 64
            self.Unknown02 = 1
            self.Unknown03 = 15
            self.DataEntry = 80
            self.ConeDriverTableEntry                = int('F0',16)
            self.ConstraintInfoEntry                 = int('F0',16)
            self.ObjectSettingEntry                  = int('330',16)
            self.SectionTableEntry                   = int('330',16)
            self.DependencyTableEntry                = int('310',16)
            self.HashTableEntry                      = int('340',16)
            self.HashTableItemCount                  = 2
            self.ConstraintCount                     = 3
            self.DependencyCount                     = 1
            self.SectionCount                        = 1

        def call_structure(self):
            return self._schema

    class Constraint_class:
        _schema = [
            ("ConeDriverList_offset", 8, hex),
            ("SourceList_offset", 8, hex, None, EntryFlag.Source),
            ("Name_offset", 8, hex, None, EntryFlag.Name),
            ("Proporty_offset", 8, hex),
            ("ObjectHash_Index", 4),
            ("ObjectHash", 4, hash),
            ("Proporty_Hash", 4, hash),
            ("ConeDriverInfoCount", 1),
            ("SourceCount", 1),
            ("Flag", 1, bin, 8),
            ("Transformation", 1, Transformation),
            ("Vector", 16, list, 4),
            ("UnknownFloat", 8, list, 4),
            ("Unknown00", 1),
            ("TransformAxis", 1, Axis),
            ("Unknown01", 1),
            ("Unknown02", 1),
            ("Unknown03", 1),
            ("Unknown04", 1),
            ("Unknown05", 1),
            ("Unknown06", 1)
        ]
        def __init__(self):
            for item in self._schema:
                if len(item) > 2:
                    match item[2]:
                        case cls if cls is list:
                            setattr(self, item[0], [0] * (item[1] // item[3]))
                        case cls if cls in (hash, hex):
                            setattr(self, item[0], '0')
                        case cls if cls is Transformation:
                            setattr(self, item[0], Transformation.Translation)
                        case cls if cls is Axis:
                            setattr(self, item[0], Axis.X)
                        case cls if cls is bin:
                            setattr(self, item[0], ['0'] * item[3])
                else:
                    setattr(self, item[0], 0)

            setattr(self, "Vector", [0, 0, 0, 1])
            self.ConeDriverList = []
            self.Name = ''
            self.Proporty = None

        def call_structure(self):
            return self._schema


    class Constraint_Source_class:

        _schema = [
            ("ComplexMappingInfoOffset", 8, hex),
            ("Name_offset", 8, hex, None, EntryFlag.Name),
            ("SourchHash_Index", 4),
            ("ComplexMappingInfoCount", 2),
            ("UnknownUInt16", 2),
            ("Updatetiming", 1, Updatetiming),
            ("Transformation", 1, Transformation_Src),
            ("Source_Axis", 1, Axis),
            ("Unknown00", 1),
            ("Unknown01", 1),
            ("Unknown02", 1),
            ("Unknown03", 1),
            ("Unknown04", 1),
            ("MapFrom", 12, list, 4),
            ("MapTo", 12, list, 4),
            ("UnknownVector", 16, list, 4),
        ]

        def __init__(self):
            for item in self._schema:
                if len(item) > 2:
                    match item[2]:
                        case cls if cls is list:
                            setattr(self, item[0], [0] * (item[1] // item[3]))
                        case cls if cls is hex:
                            setattr(self, item[0], '0')
                        case cls if cls is Updatetiming:
                            setattr(self, item[0], Updatetiming.MotionBegin)
                        case cls if cls is Transformation_Src:
                            setattr(self, item[0], Transformation_Src.Translation)
                        case cls if cls is Axis:
                            setattr(self, item[0], Axis.X)
                else:
                    setattr(self, item[0], 0)

            setattr(self,"UnknownVector",[0,0,0,1])
            self.Name = ''
            self.ConstraintList = []

        def call_structure(self):
            return self._schema

    def __init__(self):

        self.Header = self.Header_class()
        self.Constraint = []
        self.ConeDriverList = []
        self.Constraint_Source = []
        self.Constraint_Relation = {}
        self.SectionType = SectionType.Transformation

    def read_from_file(self, filename):
        with open(filename, 'rb') as jcnsfile:

            #read header
            for item in self.Header.call_structure():
                temp = jcnsfile.read(item[1])
                if len(item) > 2:
                    match item[2]:
                        case cls if cls is list:
                            temp_list = [
                                int.from_bytes(temp[i: i + item[3]], byteorder='little')
                                for i in range(0, item[1], item[3])
                            ]
                            setattr(self.Header, item[0], temp_list)
                        case cls if cls is str:
                            setattr(self.Header, item[0], temp.decode('ascii').strip('\x00'))
                        case cls if cls is hex:
                            setattr(self.Header, item[0], str(temp[::-1].hex().upper().lstrip('0')) or '0')
                else:
                    setattr(self.Header, item[0], int.from_bytes(temp, byteorder='little'))

            #read constraint
            jcnsfile.seek(int(self.Header.ConstraintInfoEntry,16),0)
            self.Constraint.append(self.Constraint_class())
            ConstraintStructure = self.Constraint[0].call_structure()
            ConstraintIndex = 0
            ConstraintSourceIndex = 0
            while True:
                for item in ConstraintStructure:
                    temp = jcnsfile.read(item[1])
                    if len(item) > 2:
                        match item[2]:
                            case cls if cls is list:
                                temp_list = [
                                    struct.unpack('<f', temp[i: i + item[3]])[0]
                                    for i in range(0, item[1], item[3])
                                ]
                                setattr(self.Constraint[ConstraintIndex], item[0], temp_list)
                            case cls if cls is hash:
                                setattr(self.Constraint[ConstraintIndex], item[0],
                                        str(temp[::-1].hex().upper().lstrip('0')))
                            case cls if cls is hex:
                                setattr(self.Constraint[ConstraintIndex], item[0],
                                        str(temp[::-1].hex().upper().lstrip('0')) or '0')
                            case cls if cls is Transformation:
                                setattr(self.Constraint[ConstraintIndex], item[0],
                                        Transformation(int.from_bytes(temp, byteorder='little')))
                            case cls if cls is Axis:
                                setattr(self.Constraint[ConstraintIndex], item[0],
                                        Axis(int.from_bytes(temp, byteorder='little')))
                            case cls if cls is bin:
                                setattr(self.Constraint[ConstraintIndex], item[0],
                                        list(f"{int.from_bytes(temp):08b}")[::-1])
                    else:
                        setattr(self.Constraint[ConstraintIndex], item[0],
                                int.from_bytes(temp, byteorder='little'))

                #read first constraint source location
                if ConstraintIndex == 0:
                    first_source_offset = self.Constraint[0].SourceList_offset

                #read constraint proporty (not finish
                if getattr(self.Constraint[ConstraintIndex], 'Proporty_offset') == '0':
                    pass

                #read constraint name
                self.Constraint[ConstraintIndex].Name = readname(self.Constraint[ConstraintIndex].Name_offset,jcnsfile)

                #read constraint source
                current_offset = jcnsfile.tell()
                jcnsfile.seek(int(self.Constraint[ConstraintIndex].SourceList_offset, 16), 0)
                for _ in range(self.Constraint[ConstraintIndex].SourceCount):
                    self.Constraint_Source.append(self.Constraint_Source_class())

                    if ConstraintSourceIndex == 0:
                        ConstraintSourceStructure = self.Constraint_Source[0].call_structure()

                    for item in ConstraintSourceStructure:
                        temp = jcnsfile.read(item[1])
                        if len(item) > 2:
                            match item[2]:
                                case cls if cls is list:
                                    temp_list = [
                                        struct.unpack('<f', temp[i: i + item[3]])[0]
                                        for i in range(0, item[1], item[3])
                                    ]
                                    setattr(self.Constraint_Source[ConstraintSourceIndex], item[0], temp_list)
                                case cls if cls is hex:
                                    setattr(self.Constraint_Source[ConstraintSourceIndex], item[0],
                                            str(temp[::-1].hex().upper().lstrip('0')) or '0')
                                case cls if cls is Updatetiming:
                                    setattr(self.Constraint_Source[ConstraintSourceIndex], item[0],
                                            Updatetiming(int.from_bytes(temp, byteorder='little')))
                                case cls if cls is Transformation_Src:
                                    setattr(self.Constraint_Source[ConstraintSourceIndex], item[0],
                                            Transformation_Src(int.from_bytes(temp, byteorder='little')))
                                case cls if cls is Axis:
                                    setattr(self.Constraint_Source[ConstraintSourceIndex], item[0],
                                            Axis(int.from_bytes(temp, byteorder='little')))
                        else:
                            setattr(self.Constraint_Source[ConstraintSourceIndex], item[0],
                                    int.from_bytes(temp, byteorder='little'))

                    self.Constraint_Source[ConstraintSourceIndex].Name = readname(self.Constraint_Source[ConstraintSourceIndex].Name_offset,jcnsfile)
                    self.Constraint_Relation.setdefault(self.Constraint[ConstraintIndex], []).append(self.Constraint_Source[ConstraintSourceIndex])
                    ConstraintSourceIndex += 1

                jcnsfile.seek(current_offset, 0)

                #finish one constraint reading
                if jcnsfile.tell() >= int(first_source_offset,16):
                    break
                else:
                    ConstraintIndex += 1
                    self.Constraint.append(self.Constraint_class())

            jcnsfile.seek(int(self.Header.ObjectSettingEntry,16), 0)
            self.SectionType = SectionType(int.from_bytes(jcnsfile.read(4), byteorder='little'))

    def write_to_file(self, filename):
        def fillentry(entryindex, parameter = None):
            current_offset = pending_data.tell()

            match entryindex:
                case EntryFlag.Source:
                    for entry in entrybus[entryindex]:
                        if entry[1] == parameter:
                            pending_data.seek(entry[0], 0)
                            pending_data.write(current_offset.to_bytes(8, byteorder='little'))

                case EntryFlag.Name | EntryFlag.DependencyHash:
                    for entry in entrybus[entryindex]:
                        if entry[1] == parameter:
                            pending_data.seek(entry[0], 0)
                            pending_data.write(current_offset.to_bytes(8, byteorder='little'))

                case EntryFlag.Constraint | EntryFlag.Dependency | EntryFlag.HashTable | EntryFlag.SectionType:
                    for entry in entrybus[entryindex]:
                        pending_data.seek(entry[0], 0)
                        pending_data.write(current_offset.to_bytes(8, byteorder='little'))

            pending_data.seek(current_offset, 0)

        def writename(name):
            temp = name.encode('utf-16le') + b'\x00\x00'
            pending_data.write(
                temp.ljust(
                    ((len(temp) + 7) // 8) * 8, b'\x00'
                )
            )

        def newline():
            pending_data.write(b'\x00' * (-pending_data.tell() % 16))

        pending_data = io.BytesIO()
        entrybus = {}

        #build hashtable
        hashtable = {}
        for constraint in self.Constraint:
            hashtable[constraint.Name] = struct.pack('<I',hash_wide(constraint.Name))
            for source in self.Constraint_Relation[constraint]:
                hashtable[source.Name] = struct.pack('<I',hash_wide(source.Name))

        # update header
        self.Header.HashTableItemCount = len(list(hashtable))
        self.Header.ConstraintCount = len(self.Constraint)
        self.Header.DependencyCount = len(set(i.Name for i in self.Constraint_Relation))

        #write header
        for item in self.Header.call_structure():
            temp = getattr(self.Header,item[0])
            if len(item) > 2:
                match item[2]:
                    case cls if cls is list:
                        pending_data.write(
                            b''.join(x.to_bytes(item[3], byteorder='little')
                                     for x in temp)
                        )
                    case cls if cls is str:
                        pending_data.write(temp.encode('ascii'))
                    case cls if cls is hex:
                        if len(item) > 4:
                            entrybus.setdefault(item[4], []).append([pending_data.tell(), None])
                        pending_data.write(b'\x00' * item[1])
            else:
                pending_data.write(temp.to_bytes(item[1], byteorder='little'))

        fillentry(EntryFlag.Constraint) #write first constraint location

        #write constraint
        ConstraintStructure = self.Constraint[0].call_structure()
        sourceindex = 0
        for index, constraint in enumerate(self.Constraint):

            #update constraint
            constraint.ObjectHash = struct.pack('<I',hash_wide(constraint.Name))
            constraint.Proporty_Hash = b'\x00\x00\x00\x00'
            constraint.ObjectHash_Index = list(hashtable).index(constraint.Name)
            constraint.SourceCount = len(self.Constraint_Relation[constraint])

            for item in ConstraintStructure:
                temp = getattr(constraint,item[0])
                if len(item) > 2:
                    match item[2]:
                        case cls if cls is list:
                            pending_data.write(
                                struct.pack(f'<{(item[1] // item[3])}f', *temp)
                            )
                        case cls if cls is hash:
                            pending_data.write(temp)

                        case cls if cls is hex:
                            if len(item) > 4:
                                match item[4]:
                                    case EntryFlag.Source:
                                        entrybus.setdefault(item[4], []).append([pending_data.tell(), sourceindex])
                                    case EntryFlag.Name:
                                        entrybus.setdefault(item[4], []).append([pending_data.tell(), constraint.Name])
                            pending_data.write(b'\x00' * item[1])

                        case cls if cls in (Transformation, Axis):
                            pending_data.write(temp.to_bytes(item[1], byteorder='little'))

                        case cls if cls is bin:
                            pending_data.write(int("".join(temp[::-1]), 2).to_bytes(1))
                else:
                    pending_data.write(temp.to_bytes(item[1], byteorder='little'))

            sourceindex += constraint.SourceCount


        #write constraint source
        SourceStructure = self.Constraint_Source[0].call_structure()
        sourceindex = 0
        for constraint in self.Constraint:
            for source in self.Constraint_Relation[constraint]:
                # update source
                source.SourchHash_Index = list(hashtable).index(source.Name)
                fillentry(EntryFlag.Source, sourceindex)
                for item in SourceStructure:
                    temp = getattr(source, item[0])
                    if len(item) > 2:
                        match item[2]:
                            case cls if cls is list:
                                pending_data.write(
                                    struct.pack(f'<{(item[1] // item[3])}f', *temp)
                                )
                            case cls if cls is hex:
                                if len(item) > 4:
                                    entrybus.setdefault(item[4], []).append([pending_data.tell(), source])
                                pending_data.write(b'\x00' * item[1])

                            case cls if cls in (Updatetiming, Transformation_Src, Axis):
                                pending_data.write(temp.to_bytes(item[1], byteorder='little'))

                    else:
                        pending_data.write(temp.to_bytes(item[1], byteorder='little'))
                sourceindex += 1

            for source in self.Constraint_Relation[constraint]:
                fillentry(EntryFlag.Name,source)
                writename(source.Name)
                if sourceindex != len(self.Constraint_Source) - 1:
                    newline()



        #write constraint name
        blacklist = []
        for constraint in list(self.Constraint_Relation):
            if constraint.Name not in blacklist:
                blacklist.append(constraint.Name)
                fillentry(EntryFlag.Name, constraint.Name)
                writename(constraint.Name)

        newline()

        #write dependency
        blacklist = []
        fillentry(EntryFlag.Dependency)
        for constraint in list(self.Constraint_Relation):
            if constraint.Name not in blacklist:
                blacklist.append(constraint.Name)
                entrybus.setdefault(EntryFlag.DependencyHash, []).append([pending_data.tell(), constraint.Name])
                pending_data.write(b'\x00' * 8)
                pending_data.write(len(set(self.Constraint_Relation[constraint])).to_bytes(8, byteorder='little'))

        blacklist = []
        for constraint in list(self.Constraint_Relation):
            source_blacklist = []
            if constraint.Name not in blacklist:
                blacklist.append(constraint.Name)
                fillentry(EntryFlag.DependencyHash, constraint.Name)
                pending_data.write(hashtable[constraint.Name])
                for source in self.Constraint_Relation[constraint]:
                    if source.Name not in source_blacklist:
                        source_blacklist.append(source.Name)
                        pending_data.write(hashtable[source.Name])

        newline()
        # write section
        fillentry(EntryFlag.SectionType)
        pending_data.write(self.SectionType.to_bytes(4, byteorder='little'))
        newline()

        #wirte hashtable
        fillentry(EntryFlag.HashTable)
        for name_hash in list(hashtable.values()):
            pending_data.write(name_hash)

        with open(filename, "wb") as f:
            f.write(pending_data.getbuffer())
            pending_data.close()