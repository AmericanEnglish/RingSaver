pyinstaller main.py       ^
    --clean               ^
    -n RingSaver          ^
    --onefile             ^
    --add-data "*.qss;."  ^
    --add-data "images/*.jpg;images/"
