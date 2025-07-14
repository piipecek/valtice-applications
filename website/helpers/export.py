from io import BytesIO
from openpyxl import Workbook
from website import db
from website.paths import logs_path, settings_path
from zipfile import ZipFile


def export() -> BytesIO:
    wb = Workbook()
    wb.remove(wb.active)
    
    for table in db.metadata.sorted_tables:
        ws = wb.create_sheet(title=table.name)
        rows = db.session.execute(table.select()).fetchall()

        ws.append([col.name for col in table.columns])

        for row in rows:
            ws.append(list(row))
            
    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)
    
    zip_stream = BytesIO()
    with ZipFile(zip_stream, 'w') as zip_file:
        zip_file.writestr('export_db.xlsx', stream.read())
        zip_file.write(logs_path(), arcname=logs_path().name)
        zip_file.write(settings_path(), arcname=settings_path().name)
    zip_stream.seek(0)
    return zip_stream

    