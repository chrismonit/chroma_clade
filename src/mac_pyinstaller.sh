pyinstaller \
--icon tree.icns \
--add-data title.png:. \
--add-data tree.png:. \
--add-data col.tree.png:. \
--add-data default_colour.csv:. \
--distpath ../apps/mac \
--workpath ../apps/mac/build \
--name ChromaClade \
--windowed \
--onefile \
--clean \
--exclude altgraph --exclude certifi --exclude chardet --exclude cycler --exclude DendroPy --exclude idna --exclude kiwisolver --exclude macholib --exclude matplotlib --exclude numpy --exclude pandas --exclude patsy --exclude pyparsing --exclude PyPDF2 --exclude python-dateutil --exclude pytz --exclude requests --exclude scikit-learn --exclude scipy --exclude setuptools --exclude six --exclude sklearn --exclude statsmodels --exclude tkcolorpicker --exclude urllib3 \
gui.py

# apparently PyInstaller 3.5 has a bug relating to tcl/tk on macOS
# compensated for by copying in files manually
# see https://github.com/pyinstaller/pyinstaller/issues/3820
cp -r ../apps/mac/lib ../apps/mac/ChromaClade.app/Contents
