import os
from pathlib import Path

def main():
    formula_shelov = '''EXT16==" - " + IF(mat_sh <> "" ; mat_sh + " - ") +IF(mat_sh1 <> "" AND mat_sh1 <> mat_sh ; mat_sh1 + " - ") +IF(mat_sh2 <> "" AND mat_sh2 <> mat_sh1 ; mat_sh2 )'''
    
    formula_convert_to_mespar_agla = '''EXT17==\
IF(PartExt20 == '@' ; '1' ; \
IF(PartExt20 == '%%' ; '2-A' ; \
IF(PartExt20 == '$' ; '2-B' ; \
IF(PartExt20 == '**' ; '3' ; \
IF(PartExt20 == '[ ]' ; '4-A' ; \
IF(PartExt20 == '[ - ]' ; '4-B' ; \
IF(PartExt20 == '@_@' ; '5' ; \
IF(PartExt20 == '&_&' ; '6' ; \
IF(PartExt20 == '#' ; '7-A' ; \
IF(PartExt20 == '##' ; '7-B' ; \
IF(PartExt20 == '###' ; '7-C' ; \
IF(PartExt20 == '####' ; '7-D' ; \
IF(PartExt20 == 'XX' ; '8' ; \
IF(PartExt20 == '~~' ; '9'))))))))))))))'''
    
    formula_semanem = '''EXT20==\
IF(INSTR(PartRemark2 ; "פרזול") OR PartMat == "סחורה" OR PartQty < 1 ; "" ; \
IF(INSTR(PartRemark2 ; "CNC") OR INSTR(PartRemark2 ; "ריפוד") ; "~~" ; \
IF(INSTR(PartRemark2 ; "הזזה") OR (degem == 1 AND INSTR(PartRef ; "דלת")) ; "@" ; \
IF(INSTR(PartRemark2 ; "OPK") OR INSTR(PartRef ; "במה") OR ((INSTR(PartRef ; "OPK") OR INSTR(PartRef ; "ק_הזזה") OR ((INSTR(PartRef ; "עליון") OR INSTR(PartRef ; "תחתון")) AND NOT INSTR(PartRef ; "צוקל") AND NOT INSTR(PartRef ; "קושר"))) AND degem == 1) ; "%%" ; \
IF(INSTR(PartRef ; "עומד") OR (INSTR(PartRef ; "מחיצה") AND (degem == 1 OR degem == 2 OR degem == 3)) ; "$" ; \
IF((degem == 4 OR degem == 5 OR degem == 6 OR degem == 8 OR degem == 9 OR degem == 11 OR degem == 12) AND INSTR(PartRef ; "דלת") AND NOT INSTR(PartRef ; "ארון") ; "[ - ]" ; \
IF((INSTR(PartRef ; "דלת") AND (degem == 2 OR degem == 3)) OR (INSTR(PartRef ; "צוקל") AND degem == 1 AND PartQty == 1) ; "[ ]" ; \
IF((INSTR(PartRef ; "קושר") OR INSTR(PartRef ; "@_@")) AND NOT INSTR(PartRemark2 ; "פרזול") AND (degem == 1 OR degem == 2 OR degem == 3) ; "@_@" ; \
IF((INSTR(PartRef ; "מדפים") OR INSTR(PartRef ; "מדף")) AND (degem == 1 OR degem == 2 OR degem == 3) ; "&_&" ; \
IF((degem == 10 OR INSTR(PartRemark2 ; "מיטות") OR INSTR(PartRef ; "ראש")) AND NOT (INSTR(PartRef ; "מגירה") OR INSTR(PartRef ; "מגרות") OR INSTR(PartRef ; "מגירות") OR PartRef == "צד_מג" OR PartRef == "מג" OR PartRef == "מג34" OR PartRef == "מג35" OR PartRef == "מג40" OR INSTR(PartRef ; "מ_תחתונה") OR INSTR(PartRef ; "צוקל") OR INSTR(PartRef ; "מראה")) ; "#" ; \
IF(INSTR(PartRef ; "מראה") AND degem == 9 ; "##" ; \
IF(INSTR(PartRef ; "צוקל") AND NOT (degem == 5 OR degem == 7 OR degem == 8 OR degem == 9) ; "###" ; \
IF(INSTR(PartRemark2 ; "מגרות") OR INSTR(PartRef ; "מגירה") OR INSTR(PartRef ; "מגרות") OR INSTR(PartRef ; "מגירות") OR PartRef == "צד_מג" OR PartRef == "מג" OR PartRef == "מג34" OR PartRef == "מג35" OR PartRef == "מג40" ; "####" ; \
IF(INSTR(PartRef ; "גירונג") ; "XX" ; "**"))))))))))))))'''

    
    formulaEXT16 = formula_shelov   #נוסחה לחומר שילוב
    formulaEXT17 = formula_convert_to_mespar_agla   #נוסחת מס' עגלה
    formulaEXT20 = formula_semanem    #נוסחת הסימנים _ הנוסחה העיקרית לזיהוי ומיון החלקים לעגלות
    
    #------------------------------------------------------------------------------------------------------------------------------------
    #STK_DIRECTORY = "2804L"
    #script_directory = os.path.dirname(os.path.abspath(__file__))
    #stk_directory = os.path.join(script_directory, STK_DIRECTORY)
    
    stk_directory = "C:/Ardis/Data/Templates/"
    updated_files_counter = 0

    for root, dirs, files in os.walk(stk_directory):
        for filename in files:
            is_degem_100 = False    #חדר שינה שלם
            f = os.path.join(root, filename)
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

                        is_formula_ext16_exist = False        
                        is_formula_ext17_exist = False 
                        is_formula_ext20_exist = False        
                                
                        for i, item in enumerate(filedata_arr):
                            if item == 'NAAM=degem' and filedata_arr[i - 1].startswith("[VRAGEN-") and filedata_arr[i+4] == 'DEFAULT=100':
                                is_degem_100 = True 
                                break
                            if item.startswith("[ISTK$FORM-"):
                                num = item.split("-")[1]
                                if num in num_counts:
                                    num_counts[num] += 1
                                else:
                                    num_counts[num] = 1
                                if num_counts[num] == 1:
                                    new_array.append(item)
                                if num_counts[num] == 2:
                                    if(is_formula_ext16_exist == False): 
                                        new_array.append(formulaEXT16)
                                        is_file_changed = True
                                    if(is_formula_ext17_exist == False): 
                                        new_array.append(formulaEXT17)
                                        is_file_changed = True
                                    if(is_formula_ext20_exist == False): 
                                        new_array.append(formulaEXT20)
                                        is_file_changed = True
                                    new_array.append(item)
                                    is_formula_ext16_exist = False        
                                    is_formula_ext17_exist = False        
                                    is_formula_ext20_exist = False
                            elif(item.startswith("EXT16")):
                                is_formula_ext16_exist=True
                                if(item != formulaEXT16):
                                    new_array.append(formulaEXT16)
                                    is_file_changed = True
                                else:
                                    new_array.append(item)
                            elif(item.startswith("EXT17")):
                                is_formula_ext17_exist=True
                                if(item != formulaEXT17):
                                    new_array.append(formulaEXT17)
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
                        if(is_degem_100):
                            file.write('\n'.join(filedata_arr))
                        else:
                            updated_files_counter += 1
                            file.write('\n'.join(new_array))
                            
                            

            if(is_file_changed == True and is_degem_100 == False):
                print("File updated: " , f)
            
    
    
    print("-----------------------------------------------------------------")        
    print("-----------------------------------------------------------------")        
    print("Number of files updated: " , updated_files_counter)        
    input("Press enter to exit;")
            

    
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    main()
