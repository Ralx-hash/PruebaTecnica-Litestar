import sys
from pathlib import Path

#este archivo se encarga de agregar el directorio raíz del proyecto al sys.path para que los 
#módulos puedan ser importados correctamente durante las pruebas. 
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
