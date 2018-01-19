import sys
import json
import xlsxwriter


sections = json.load(open(sys.argv[1],encoding="utf-8"))["sections"]
term = "T1"

workbook = xlsxwriter.Workbook(sys.argv[2])
bold = workbook.add_format({'bold': True})
# percentage = workbook.add_format({'num_format': '##.##%'})

for section in sections:
    if section["finalGrades"] is None: continue
    grade = float(section["finalGrades"][term]["percent"])
    if grade == 0.0: continue
    worksheet = workbook.add_worksheet(section["name"].replace(":","")[:31])
    first_row = ["Name","Score","Max Score","Weight","Standardized Score","Standardized Max Score","Actual Weight","Type","","Weight"]
    cur_x = 0
    for i in first_row:
        worksheet.write(0, cur_x, i, bold)
        cur_x+=1
        
    assignments = section["assignments"]
    cur_y = 2
    
    categories=set()
    # lines
    for i in assignments:
        worksheet.write(cur_y-1, 0, i["name"])
        worksheet.write(cur_y-1, 1, float(i["score"]) if i["score"]!="--" else "--")
        worksheet.write(cur_y-1, 2, float(i["pointsPossible"]))
        worksheet.write(cur_y-1, 3, float(i["weight"]))
        worksheet.write(cur_y-1, 4, "=D%d*B%d"%(cur_y,cur_y))
        worksheet.write(cur_y-1, 5, "=D%d*C%d"%(cur_y,cur_y))
        worksheet.write(cur_y-1, 6, "=F%d/F%d"%(cur_y,len(assignments)+2))
        worksheet.write(cur_y-1, 7, i["category"])
        categories.add(i["category"])

        cur_y+=1
    # total
    worksheet.write(cur_y-1, 0, "Total", bold)
    worksheet.write(cur_y-1, 1, "=SUM(B2:B%d)"%(cur_y-1))
    worksheet.write(cur_y-1, 2, "=SUM(C2:C%d)"%(cur_y-1))
    worksheet.write(cur_y-1, 4, '=SUMIF(E2:E%d,"<>#VALUE!")'%(cur_y-1))
    worksheet.write(cur_y-1, 5, '=SUMIF(E2:E%d,"<>#VALUE!",F2:F%d)'%(cur_y-1,cur_y-1))
    cur_y+=1
    worksheet.write(cur_y-1, 4, "Percentage")
    worksheet.write(cur_y-1, 5, "=E%d/F%d"%(len(assignments)+2,len(assignments)+2), bold)
    # weight
    cur_y=2
    for cat in categories:
        worksheet.write(cur_y-1, 8, cat)
        sum=0
        for i in assignments:
            worksheet.write(cur_y-1, 9, "=SUMIF(H2:H%d,I%d,G2:G%d)"%(len(assignments)+1,cur_y,len(assignments)+1))
        cur_y+=1

workbook.close()
