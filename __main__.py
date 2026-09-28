import os
import modules.jcns_main as jcns

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

def catjcns(jcns_class):

    print('---------HEADER----------')
    for item in jcns_class.Header.call_structure():
        print(f'{item[0]} : {getattr(jcns_class.Header, item[0])}')

    print('\n-------CONSTRAINTS-------')
    for constraint in jcns_class.Constraint:
        print(f'Name : {"".join(getattr(constraint, 'Name'))}')
        for item in constraint.call_structure():
            print(f'{item[0]} : {getattr(constraint, item[0])}')
        print('')

        print('    ----CONNECTED_SOURCE-----')
        for constraint_Src in jcns_class.Constraint_Relation[constraint]:
            print(f'    Name : {getattr(constraint_Src, 'Name')}')
            for item in constraint_Src.call_structure():
                print(f'    {item[0]} : {getattr(constraint_Src, item[0])}')
            print('')

    print('-----OBJECT_SETTING------')
    print(f'SectionType : {jcns_class.SectionType}')

def make_my_jcns():
    test = jcns.jcns_class()
    constraint_name = ['HJ_0_C','HJ_0_F','HJ_1_C','HJ_1_F','HJ_2']
    source_name = ['R_Blade','Emblem','L_Blade','Emblem','Emblem']
    for index, name in enumerate(constraint_name):
        test.Constraint.append(jcns.jcns_class.Constraint_class())
        test.Constraint[index].Name = f'{name}'

    for index, name in enumerate(source_name):
        test.Constraint_Source.append(jcns.jcns_class.Constraint_Source_class())
        test.Constraint_Source[index].Name = f'{name}'

    for i in range(5):
        test.Constraint_Relation.setdefault(test.Constraint[i], []).append(test.Constraint_Source[i])

    test.write_to_file("test.jcns.102")
    print('Finish writing')

make_my_jcns()