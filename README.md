# taller-isi
tp isi
Diagrama de clases UML: Plataforma de Preguntas y Respuestas con Agente de IA

Integrantes: Santiago Juarez, Justo Campoy, Enzo Mercado, Santiago Miloch

Qué se hizo con draw.io

Para este trabajo realizamos el diagrama de clases UML de nuestro sistema utilizando draw.io (diagrams.net). En el diagrama modelamos las clases con sus atributos y métodos, las interfaces, las clases abstractas y las relaciones entre ellas: herencia, realización de interfaces, asociaciones con su multiplicidad, dependencias y agregación. Para distinguir los elementos usamos la notación UML estándar: los estereotipos «interface» y «abstract», el nombre en cursiva para las clases abstractas, y los signos - y + para indicar visibilidad privada o pública.

Junto con este documento se entrega el archivo editable diagrama_clases.drawio, que se abre desde app.diagrams.net con la opción "Abrir diagrama existente", y una imagen diagrama-jpeg para poder verlo sin necesidad de abrir la herramienta.

Funcionalidad del sistema

El sistema modelado es una plataforma de preguntas y respuestas, parecida a un foro técnico. Los usuarios publican preguntas, otros les responden y la comunidad vota tanto las preguntas como las respuestas. Además, una respuesta puede ser escrita por una persona o generada automáticamente por un agente de inteligencia artificial.

Una Pregunta tiene título, cuerpo y fecha de publicación, y es formulada por un Usuario. Cada pregunta pertenece a una Categoria y puede tener varios Tag, de modo que una etiqueta puede aparecer en muchas preguntas. Una pregunta puede recibir muchas Respuesta, y cada respuesta guarda su cuerpo, su fecha y un atributo esAceptada que permite marcar cuál fue la que resolvió la consulta.

Para los votos definimos la interfaz Votable, que implementan tanto Pregunta como Respuesta. La clase Voto guarda un valor entero y se asocia a un elemento votable y al usuario que lo emitió. De esta forma el mismo mecanismo de votación sirve para preguntas y respuestas sin duplicar código.

Quien escribe una respuesta se representa con la clase abstracta Autor, que define el método obtenerNombre(). De ella heredan Usuario (con email y contraseña, que a su vez se especializa en Admin y UsuarioGeneral) y AgenteIA. Gracias a esto, Respuesta solo necesita conocer un Autor, sin importar si quien responde es una persona o la inteligencia artificial.

El AgenteIA genera respuestas mediante el método generarRespuesta(pregunta), pero no produce el texto por sí mismo: delega en un GeneradorRespuesta, una interfaz con el método generar(pregunta). Esa interfaz tiene tres implementaciones, OpenAIStrategy, GeminiStrategy y ModeloLocalStrategy, que representan distintos proveedores de IA. Así se puede cambiar de proveedor sin modificar al agente.

Por último, AutorFactory se encarga de crear los autores a través del método crearAutor(tipo), devolviendo el tipo de autor que corresponda, ya sea un usuario o un agente de IA.

Patrones de diseño y principios aplicados

Aplicamos dos patrones de diseño. El patrón Strategy está en la interfaz GeneradorRespuesta y sus tres implementaciones, usadas por AgenteIA, y permite intercambiar el proveedor de IA sin tocar el resto del sistema. El patrón Factory está en AutorFactory, que centraliza la creación de autores y evita que el resto del código dependa de las clases concretas.

También se aprovechan principios de la programación orientada a objetos: herencia en Autor y Usuario, abstracción mediante clases abstractas e interfaces, y polimorfismo en Votable, Autor y GeneradorRespuesta.

Conclusión

El diagrama representa una plataforma donde los usuarios publican y votan contenido, y donde las respuestas pueden venir de personas o de un agente de IA configurable. El diseño con Strategy y Factory deja el sistema flexible: se puede agregar un nuevo proveedor de IA o un nuevo tipo de autor sin modificar las demás clases.
