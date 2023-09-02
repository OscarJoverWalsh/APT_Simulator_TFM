# APT_Simulator_TFM

## Tabla de contenido
* [Información general](#información-general)
* [Tecnologías](#tecnologías)
* [Instalación](#instalación)
* [Ejecución](#ejecución)


## Información General
Como solución se propone el desarrollo de un proyecto para el modelado y simulación de APTs basada en inteligencia artificial, para su uso en pruebas de penetración en entornos simulados. El proceso de generación del modelo se basa en la construcción de cadenas de habilidades aplicando el algoritmo de aprendizaje por refuerzo Q-Learning. Este proyecto tiene como objetivo la definición formal de los modelos que permitan caracterizar los APTs siguiendo el estándar MITRE.
Esta herramienta ha sido desarrollada y probada en versiones previas para su implementación en el proyecto COBRA. Este proyecto, financiado por el Mando Conjunto del Ciberespacio (MCCE) del gobierno Español, está orientado al desarrollo de cibermaniobras adaptables y personalizables de simulación hiperrealista de APT, así como entrenamiento en ciberdefensa a través de la gamificación. COBRA.


## Tecnologías
El proyecto se ha creado utilizando las siguientes tecnologías:
* Python versión ````3.7.9````
* VirtualBox: Software de virtualización desarrollado por Oracle Corporation que permite crear y gestionar máquinas virtuales aisladas en un entorno de máquina host. [Pagina oficial]([https://attack.mitre.org/](https://www.virtualbox.org/)) de VirtualBox.
* MITRE ATT&CK® (Adversarial Tactics, Techniques, and Common Knowledge): herramienta dedicada a la comprensión y clasificación de tácticas, técnicas y procedimientos (TTPs) empleados por adversarios en los ciberataques. [Pagina oficial](https://attack.mitre.org/) de MITRE.
* CALDERA ````4.1````: proyecto de ciberseguridad desarrollado por MITRE Corporation que se basa en el marco MITRE ATT&CK. CALDERA es una plataforma diseñada para realizar simulaciones de ataques y pruebas de penetración. Para más información, acceda a la [documentación](https://caldera.readthedocs.io/en/latest/) oficial de CALDERA.


## Instalación
* Previo a la instalación del proyecto, deberá tener instalado el software de virtualización virtualBox. Para más información en como instalar esta herrmaineta, acceda a este enlace: [Pagina oficial]([https://attack.mitre.org/](https://www.virtualbox.org/)) de VirtualBox. Adicionalmente, deberá contar con una máquina Linux Ubunutu donde se despelgará la herrmianta y servidor CALDERA. Para la creación de máquinas víctimas, deberá contar con una máquina virtual Linux Ubuntu o windows. El escenario simulado en este proyecto consiste en una máquina atacante Linux Ubuntu 20.04 que alberga la herramienta de simulación de APTs y una máuquina Linux Ubuntu 22.04, donde se desplegará la víctima.
* Adicionalmente, se deberá instalar python en ambas máquinas.
```$ sudo apt install python3```
**Nota:** Para comprobar la versión de python instalada, puede ejecutar el siguiente comando: ```python3 -verison```.

Para el arranque del proyecto deberá:
* En la máquina atacante deberá instalar la carpeta envSimulators. Esta carteta contiene la herrmianta de modelado de APTs aplicando algoritmos de aprendizaje por refuerzo ```APTSimulator_V2``` y la herrmianta empleada para la simulación de APTs ```caldera4.1```. El directorio se podrá descargar de forma manual o através de el siguiente comnado.
```$ sudo apt-get install https://github.com/OscarJoverWalsh/APT_Simulator_TFM.git```
* En la máquina víctima deberá instalar la carpeta Agent. Esta contiene el script necesario para conectar el agente con el servidor CALDERA.


## Ejecución
Previo a la ejecución, será necesario modificar la dirección en la que se almacena la base de datos dentro en el equipo local. Deberá introducir en ```APTModelGenerator``` la ruta completa del fichero ```APT_Data_Model_ddbb.sqlite```.

Una vez instaldo el programa y realizados los cambios anterioriormente descritos, se podrá ejecutar desde el terminal con el siguiente comando.

```$ python APTModelGenerator.py```.

Paso seguido, el programa solicitará introducir el número de patrones de ataque que se desean extraer en la consulta a la base de datos de ATTA&CK. El resultado de esta ejecución es un fichero de nombre ```APTModelGenerated.json``` con el modelo APT generado. 

Para la representación gráfica de los distintos componentes que constituyen el modelo, el fichero generado deberá introducirse en el [visualizador STIX](https://oasis-open.github.io/cti-stix-visualization/n).
