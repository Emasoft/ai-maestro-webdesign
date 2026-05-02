## Table of Contents

- [Ejemplo de concepto: "Modernismo, Generación del 98 y Vanguardias — clase de literatura"](#ejemplo-de-concepto-modernismo-generación-del-98-y-vanguardias-clase-de-literatura)
- [Notas sobre esta estructura](#notas-sobre-esta-estructura)


# Prompt template (Spanish) — ejemplo ya completo

Ejemplo completo con la forma del prompt que el skill envía a Gemini. Úsalo
tal cual como punto de partida y sustituye los placeholders `<entre ángulos>`
por el concepto del usuario. El prompt que la API verá es todo lo que hay
entre los bloques vallados a continuación.

## Ejemplo de concepto: "Modernismo, Generación del 98 y Vanguardias — clase de literatura"

```
Genera una ilustración estilo Excalidraw / hand-drawn de ALTA CALIDAD para material educativo EN ESPAÑOL.

FORMATO: Panorámico 16:9.

ESTILO VISUAL:
- Trazos sueltos pero DETALLADOS y expresivos, como un ilustrador profesional
- Fondo blanco limpio
- Paleta: negro para trazos, azul claro para MODERNISMO, naranja suave para GENERACIÓN DEL 98, verde menta para VANGUARDIAS
- Todo el texto dentro de MARCOS REDONDEADOS, BOCADILLOS o ETIQUETAS CON FONDO relleno
- Flechas grandes estilo hand-drawn conectando los tres paneles
- Sombreado con trazos cruzados para dar profundidad

COMPOSICIÓN:
Tres paneles verticales de izquierda a derecha, separados por líneas hand-drawn finas. Cada panel tiene un marco de título arriba, una ilustración central con muchos iconos pequeños, un bocadillo, 2-3 iconos etiquetados y un marco inferior con los autores representativos. En la parte inferior de la imagen, una línea temporal hand-drawn con marcadores de fecha.

PANEL 1 (izquierda — MODERNISMO, paleta azul claro):
- Título «MODERNISMO» en marco redondeado con fondo azul claro, letras grandes
- Ilustración central: un cisne estilizado junto a un lirio y una columna clásica, trazos sueltos
- Bocadillo: «Belleza y evasión»
- Iconos etiquetados en marcos: cisne («símbolo»), paleta de colores («sinestesia»), lira («musicalidad»)
- Marco inferior: «Rubén Darío · Valle-Inclán · Juan Ramón Jiménez»

PANEL 2 (centro — GENERACIÓN DEL 98, paleta naranja suave):
- Título «GEN. DEL 98» en marco redondeado con fondo naranja, letras grandes
- Ilustración central: un paisaje de Castilla con una encina solitaria y un camino polvoriento, trazos sueltos con sombreado cruzado
- Bocadillo: «España en crisis»
- Iconos etiquetados en marcos: encina («Castilla»), pluma («ensayo»), bandera rota («1898»)
- Marco inferior: «Unamuno · Machado · Baroja · Azorín»

PANEL 3 (derecha — VANGUARDIAS, paleta verde menta):
- Título «VANGUARDIAS» en marco redondeado con fondo verde menta, letras grandes
- Ilustración central: un collage cubista de formas geométricas con un ojo, un reloj derretido y líneas que se fragmentan, trazos expresivos
- Bocadillo: «Ruptura total»
- Iconos etiquetados en marcos: cubo («cubismo»), rayo («futurismo»), máscara («surrealismo»)
- Marco inferior: «Lorca · Alberti · Guillén · Salinas»

CONEXIONES:
- Flechas hand-drawn grandes de panel a panel, con etiquetas: «reacción» entre PANEL 1 y PANEL 2, «experimenta» entre PANEL 2 y PANEL 3
- Línea temporal hand-drawn en la parte inferior con marcadores: «1888», «1898», «1914», «1927»

REGLAS DE TEXTO — VERIFICAR LETRA POR LETRA:
- MODERNISMO se escribe M-O-D-E-R-N-I-S-M-O
- GEN. DEL 98 se escribe G-E-N punto espacio D-E-L espacio 9-8
- VANGUARDIAS se escribe V-A-N-G-U-A-R-D-I-A-S
- RUBÉN DARÍO se escribe R-U-B-É-N espacio D-A-R-Í-O (con tilde en la E y en la I)
- VALLE-INCLÁN se escribe V-A-L-L-E guión I-N-C-L-Á-N (con tilde en la A)
- UNAMUNO se escribe U-N-A-M-U-N-O
- MACHADO se escribe M-A-C-H-A-D-O
- BAROJA se escribe B-A-R-O-J-A
- AZORÍN se escribe A-Z-O-R-Í-N (con tilde en la I)
- LORCA se escribe L-O-R-C-A
- ALBERTI se escribe A-L-B-E-R-T-I
- GUILLÉN se escribe G-U-I-L-L-É-N (con tilde en la E)
- SALINAS se escribe S-A-L-I-N-A-S
- Cada palabra debe estar PERFECTAMENTE ESCRITA en español correcto, con todas las tildes en su sitio
- El texto debe ser GRANDE y LEGIBLE
- Máximo 2-3 palabras por etiqueta
- Todo texto siempre dentro de un marco o bocadillo, nunca flotando

Imita fielmente el estilo visual de las imágenes de referencia proporcionadas.
```

## Notas sobre esta estructura

- **El bloque de deletreo no es opcional.** Sin él, Gemini renombra a «Unamuno»
  como «Umaruno» o pierde las tildes. El pase de ortografía es la palanca de
  calidad más grande.
- **Tres acentos, uno por panel.** Cuatro paletas distintas se leen como ruido.
  Si hay un cuarto concepto, conviene una segunda ilustración separada.
- **Los autores van en un marco inferior etiquetado.** Nombres de autores
  flotando se ven como IA-slop; enmarcados parecen apunte del profesor.
- **Tildes explícitas en el deletreo.** La API obedece: si el deletreo dice
  «con tilde en la I», la tilde aparece. Si lo omites, la tilde se pierde
  la mitad de las veces.
