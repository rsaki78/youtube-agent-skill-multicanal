# Empezar un canal desde cero

Guía para quien usa el plugin por primera vez y todavía no tiene canal. El plugin no publica nada:
te acompaña en cada decisión, en orden, y te entrega todo listo para que tú lo copies y lo subas.

## Antes de empezar

1. **Claude Code** instalado.
2. **Python 3** - compruébalo con `python3 --version` (en Windows puede ser `py --version`).
3. **yt-dlp** - `pip install yt-dlp`. Sirve para investigar otros canales; solo lee páginas
   públicas, nunca entra a tu cuenta.
4. **Una cuenta de Google** - la vas a necesitar en el paso 3 para crear el canal.

## Instalación (una vez por canal)

Cada canal vive en su propia carpeta, con sus propias skills y su propia voz:

```bash
git clone https://github.com/rsaki78/youtube-agent-skill-multicanal.git
mkdir -p mi-canal/.claude/skills
cp -r youtube-agent-skill-multicanal/skills/yt-* mi-canal/.claude/skills/
```

O como plugin, desde la carpeta del canal:

```bash
claude plugin marketplace add rsaki78/youtube-agent-skill-multicanal
claude plugin install youtube-agent-multicanal@youtube-agent-skill-multicanal --scope project
```

Los archivos de `.claude/youtube/` (`channel.md`, `voice.md`) los crea `/yt-launch` la primera vez.

Las herramientas se corren con `python3`. En Windows, si ese comando no existe, usa `py` o `python`.

Abre Claude Code dentro de `mi-canal` y escribe:

```
/yt-launch
```

Desde aquí el plugin te guía. Hace **un paso por sesión**. Cuando vuelvas otro día, escribe
`/yt-launch` de nuevo y retoma donde te quedaste: todo queda guardado en
`.claude/youtube/channel.md`.

## Los seis pasos

### 1. Nicho y subnicho - `/yt-niche`

**Tú:** respondes cinco preguntas - de qué podrías hacer 100 videos, qué sabes que otros no, si
sales a cámara o será un canal sin cara (con tu voz, con un narrador o con voz IA), cuántas
horas tienes a la semana, para qué país e idioma, y para qué quieres el
canal. De 20 títulos que te propone, marcas los que sí harías.

**Claude:** investiga canales reales de cada nicho candidato y te dice si hay espacio: si los
canales pequeños todavía logran videos muy por encima de su promedio. Luego acota a un subnicho y
escribe tus primeros 10 títulos.

**Resultado:** una frase como *"finanzas personales para freelancers que cobran en dólares en
México"*.

### 2. Canales de referencia - `/yt-refs`

**Tú:** le dices qué canales del tema ya ves.

**Claude:** te da de 6 a 10 canales en tres grupos - los grandes que marcan el estándar, los de tu
tamaño que están creciendo (los más útiles) y los de otro tema que ve tu mismo público - con **una
cosa concreta que copiar** de cada uno y otra que no.

### 3. Nombre y handle - `/yt-name`

**Tú:** dices si tu cara será la marca. Eliges uno de cinco nombres, cada uno con su @handle ya
revisado contra YouTube.

**Ese mismo día creas el canal** con ese nombre y ese handle:

- **Sin canal todavía:** en youtube.com, con tu sesión iniciada, menú de tu foto de perfil →
  *Crear un canal*.
- **Ya tienes un canal personal** y quieres este aparte: configuración de YouTube → *Agregar o
  administrar tus canales* → *Crear un canal nuevo*.

Crear el canal no publica nada; queda vacío hasta tu primer video. Pero un handle libre deja de
estarlo en cuanto otro lo toma.

### 4. Tu voz y tu estilo - `/yt-voice`

**Tú:** grabas con el celular dos audios de 2-3 minutos, sin guion: uno explicándole a un amigo uno
de tus 10 títulos, otro contando algo del tema que te salió mal. Los transcribes - con el dictado
del celular, o subiéndolos como video oculto a YouTube - y le pasas el texto.

**Claude:** mide cómo hablas - si tratas de tú o de usted, tus frases repetidas, tus muletillas, tu
velocidad - y escribe dos archivos:

- **`voice.md`** - cómo suenas. Desde aquí, todos los guiones se escriben con tu voz.
- **`style.md`** - duración de los videos, cuántos por semana, tus 3-4 tipos de video y qué métricas
  mirar.

**¿Canal con narrador o voz IA?** No grabas la prueba de voz: defines al personaje que narra (cómo
habla, cómo trata al espectador) y, con voz IA, la configuración de la voz y la lista de palabras
que debe pronunciar bien. Después Claude mide la primera narración para fijar el ritmo de los guiones.

### 5. Logo y banner - `/yt-brand`

**Tú:**

1. Eliges una de 2-3 direcciones visuales: paleta, tipografía, idea del logo.
2. Pegas los prompts que te da en tu generador de imágenes favorito - ChatGPT, Gemini, Midjourney.
3. Guardas las imágenes en `.claude/youtube/brand/` y abres `preview.html`: ves tu canal como en
   computadora, celular y TV, y tu logo del tamaño de un comentario.
4. Pones el texto del banner sobre la plantilla que te deja, en Canva o Figma, para que quede
   dentro de la zona que se ve en celular.
5. Subes logo y banner en YouTube Studio.

### 6. Descripción y configuración - `/yt-about`

**Tú:** eliges entre dos borradores de descripción - máximo 1000 caracteres, ya revisados - y la
pegas en Studio.

**Claude:** te da la lista de lo que falta configurar: enlaces, correo de contacto, país, idioma y
los textos predeterminados de tus videos.

## Cuando terminas

Tu canal existe, pero no está lanzado. Sigue con:

1. `/yt-plan` - el primer mes, ajustado a tus horas reales.
2. `/yt-script` - tu primer video, a partir de uno de tus 10 títulos.
3. **Ten grabado el segundo video antes de publicar el primero.** Que el ritmo no se rompa en la
   segunda semana.

## Consejos

- **¿Ya tienes algo?** Un nombre, un logo: díselo. No lo descarta, pero lo revisa igual.
- **¿Cambias de opinión** en algo ya cerrado? El plugin te avisa qué pasos posteriores hay que
  revisar.
- **Cualquier paso funciona solo** - por ejemplo, únicamente `/yt-name`.
- **Nada se publica solo.** Cada paso termina con la pregunta *"ship it, or change it?"*.

## Qué archivos vas a tener al final

```
mi-canal/.claude/youtube/
  channel.md      el registro de cada decisión y por qué
  voice.md        cómo suenas
  style.md        cómo se hace el canal
  research/       los datos de los canales investigados
  brand/          prompts, plantilla del banner, vista previa, logo y banner finales
```
