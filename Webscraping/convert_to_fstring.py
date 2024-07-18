import pandas as pd

df = pd.read_csv('.\outputs\srh_masters_course_content.csv', index_col='Name')

def create_course_fstring(row):
  fstring_course = ''
  course = row.name
  for field, info in zip(row.index[:], row.values):
    fstring_field = f'{course} {field} {info}. '
    fstring_course += fstring_field
  return fstring_course

final_fstring = ''
for i in df.index:
  final_fstring += create_course_fstring(df.loc[i, :])

f = open(".\outputs\srh_course_content_fstring.txt", "a")
f.write(final_fstring)
f.close()