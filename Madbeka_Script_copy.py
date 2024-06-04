import os
from pathlib import Path

def main():
    STK_DIRECTORY = "2804L"
    #formulaEXT19 = "EXT19==IF(mat_sh1 <> '' ; 'X')"
    #formulaEXT20 = "EXT20==IF(INSTR(PartRef ;'AMOD') ; '@')"
    #formulaEXT19 = "EXT19==XXXX19"
    #formulaEXT20 = "EXT20==YYYY20"
    formulaEXT17 = '''EXT17==IF(PartExt20 == '@' ; 1 ; IF(PartExt20 == '%%' ; 2.1 ; IF(PartExt20 == '$' ; 2.2 ; IF(PartExt20=='**' ; 3 ; IF(PartExt20=='[ ]' ; 4 ; IF(PartExt20=='@_@' ; 5; IF(PartExt20=='&_&' ; 6 ; IF(PartExt20=='#' ; 7.1 ; IF(PartExt20=='##' ; 7.2 ; IF(PartExt20=='###' ; 7.3 ; IF(PartExt20=='####' ; 7.4 ; IF(PartExt20=='XX' ; 8 ; IF(PartExt20=='~~' ; 9))))))))))))) '''
    formulaEXT19 = '''EXT19==" - " + IF(mat_sh <> "" ; mat_sh + " - ") +IF(mat_sh1 <> "" AND mat_sh1 <> mat_sh ; mat_sh1 + " - ") +IF(mat_sh2 <> "" AND mat_sh2 <> mat_sh1 ; mat_sh2 )'''
    formulaEXT20 = '''EXT20==IF( INSTR(PartRemark2 ; 'פרזול') ; '' ;  IF( INSTR(PartRemark2 ; 'הזזה') ; '@' ; IF( INSTR(PartRemark2 ; 'OPK') OR (INSTR(PartRef; 'במה') AND INSTR(motsar;'הזזה') ) ; '%%'; IF( INSTR(PartRef ; 'עומד') ; '$'; IF(; '**' ;  IF( INSTR(PartRef ; 'דלת') AND INSTR(motsar ; 'הזזה') == 0 ; '[ ]' ; IF( (INSTR(PartRef ; 'קושר') OR INSTR(PartRef ; '@_@')) AND INSTR(PartRemark2 ; 'פרזול') == 0 ; '@_@' ; IF( INSTR(PartRef ; 'מדפים') ; '&_&' ; IF( INSTR(PartRemark2; 'מיטות') AND INSTR(PartRef; 'צוקל')==0 AND INSTR(PartRef ; 'מראה')==0  AND (PartRef; 'מגירה') == 0  ; '#' ; IF( INSTR(PartRef; 'מראה') AND INSTR(PartRemark2; 'מיטות') ; '##' ; IF( INSTR(PartRef; 'צוקל') AND INSTR(motsar; 'הזזה') == 0 ; '###' ; IF( INSTR(PartRemark2; 'מגרות') OR INSTR(PartRef ; 'מגירה') ; '####' ; IF(INSTR(PartRef ; 'גירונג') OR (INSTR(PartRef ; 'צוקל') AND INSTR(motsar; 'הזזה')) ; 'XX' ; IF( INSTR(PartRemark2 ; 'CNC') OR INSTR(PartRemark2; 'ריפוד') ; '~~' ) ) ) ) ) ) ) ) ) ) ) ) )  ) '''
    
    script_directory = os.path.dirname(os.path.abspath(__file__))
    stk_directory = os.path.join(script_directory, STK_DIRECTORY)

    for filename in os.listdir(stk_directory):
        f = os.path.join(stk_directory, filename)
        print(f)
        is_file_changed = False
        if os.path.isfile(f):
            if f.endswith('.STK'):
                with open(f, 'r') as file:
                    filedata = file.read()
                    ##
                    #filedata_arr_str = filedata.decode("utf-8", errors="ignore")
                    ##
                    filedata_arr= filedata.split('\n')
                    
                    new_array = []
                    num_counts = {}

                    is_formula_ext17_exist = False 
                    is_formula_ext19_exist = False        
                    is_formula_ext20_exist = False        
                            
                    for item in filedata_arr:
                        if item.startswith("[ISTK$FORM-"):
                            num = item.split("-")[1]
                            if num in num_counts:
                                num_counts[num] += 1
                            else:
                                num_counts[num] = 1
                            if num_counts[num] == 1:
                                new_array.append(item)
                            if num_counts[num] == 2:
                                if(is_formula_ext17_exist == False): 
                                    new_array.append(formulaEXT17)
                                    is_file_changed = True
                                if(is_formula_ext19_exist == False): 
                                    new_array.append(formulaEXT19)
                                    is_file_changed = True
                                if(is_formula_ext20_exist == False): 
                                    new_array.append(formulaEXT20)
                                    is_file_changed = True
                                new_array.append(item)
                                is_formula_ext19_exist = False        
                                is_formula_ext20_exist = False
                        elif(item.startswith("EXT17")):
                            is_formula_ext17_exist=True
                            if(item != formulaEXT17):
                                new_array.append(formulaEXT17)
                                is_file_changed = True
                            else:
                                new_array.append(item)
                        elif(item.startswith("EXT19")):
                            is_formula_ext19_exist=True
                            if(item != formulaEXT19):
                                new_array.append(formulaEXT19)
                                is_file_changed = True
                            else:
                                new_array.append(item)
                        elif(item.startswith("EXT20")):
                            is_formula_ext20_exist=True
                            if(item != formulaEXT20):
                                new_array.append(formulaEXT20)
                                is_file_changed = True
                            else:
                                new_array.append(item)
                        else:
                            new_array.append(item)
               
                    
                with open(f, 'w') as file:
                    file.write('\n'.join(new_array))

        if(is_file_changed == True):
            print("File Changed: " , f)
            
            
    input("Press enter to exit;")
            

    
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    main()