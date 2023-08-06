# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notas_musicais']

package_data = \
{'': ['*']}

install_requires = \
['rich>=13.2.0,<14.0.0', 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['notas-musicais = notas_musicais.cli:app']}

setup_kwargs = {
    'name': 'notas-musicais',
    'version': '0.2.0',
    'description': 'Notas musicais é um CLI para ajudar na formação de escalas, acordes e campos harmônicos',
    'long_description': '<img src="https://notas-musicais.readthedocs.io/en/latest/assets/logo.png" width="200">\n\n# Notas musicais\n[![Documentation Status](https://readthedocs.org/projects/notas-musicais/badge/?version=latest)](https://notas-musicais.readthedocs.io/en/latest/?badge=latest)\n![CI](https://github.com/dunossauro/notas-musicais/actions/workflows/pipeline.yaml/badge.svg)\n[![codecov](https://codecov.io/gh/dunossauro/notas-musicais/branch/main/graph/badge.svg?token=OVQQF4IQY2)](https://codecov.io/gh/dunossauro/notas-musicais)\n\nNotas musicais é um CLI para ajudar na formação de escalas, acordes e campos harmônicos.\n\nToda a aplicação é baseada em um comando chamado `notas-musicais`. Esse comando tem um subcomando relacionado a cada ação que a aplicação pode realizar. Como `escalas`, `acordes` e `campo-harmonico`\n\n## Instalação\n\nPara instalação do cli do projeto recomendamos que use o `pipx` para fazer essa instalação:\n\n```bash\npipx install notas-musicais\n```\n\nEmbora isso seja somente uma recomendação! Você também pode instalar o projeto com o gerenciador de sua preferência. Como o pip:\n\n```bash\npip install notas-musicais\n```\n\n## como usar?\n\n### Escalas\n\nVocê pode chamar as escalas via linha de comando. Por exemplo:\n\n\n```bash\nnotas-musicais escala\n```\n\nRetornando os graus e as notas correspondentes a essa escala:\n\n```\n┏━━━┳━━━━┳━━━━━┳━━━━┳━━━┳━━━━┳━━━━━┓\n┃ I ┃ II ┃ III ┃ IV ┃ V ┃ VI ┃ VII ┃\n┡━━━╇━━━━╇━━━━━╇━━━━╇━━━╇━━━━╇━━━━━┩\n│ C │ D  │ E   │ F  │ G │ A  │ B   │\n└───┴────┴─────┴────┴───┴────┴─────┘\n```\n\n#### Alteração da tônica da escala\n\nO primeiro parâmetro do CLI é a tônica da escala que deseja exibir. Desta forma, você pode alterar a escala retornada. Por exemplo, a escala de `F#`:\n\n```bash\nnotas-musicais escala F#\n```\n\nResultado em:\n\n```\n┏━━━━┳━━━━┳━━━━━┳━━━━┳━━━━┳━━━━┳━━━━━┓\n┃ I  ┃ II ┃ III ┃ IV ┃ V  ┃ VI ┃ VII ┃\n┡━━━━╇━━━━╇━━━━━╇━━━━╇━━━━╇━━━━╇━━━━━┩\n│ F# │ G# │ A#  │ B  │ C# │ D# │ F   │\n└────┴────┴─────┴────┴────┴────┴─────┘\n```\n\n#### Alteração na tonalidade da escala\n\nVocê pode alterar a tonalidade da escala também! Esse é o segundo parâmetro da linha de comando. Por exemplo, a escala de `D#` maior:\n\n```\nnotas-musicais escala D# menor\n\n┏━━━━┳━━━━┳━━━━━┳━━━━┳━━━━┳━━━━┳━━━━━┓\n┃ I  ┃ II ┃ III ┃ IV ┃ V  ┃ VI ┃ VII ┃\n┡━━━━╇━━━━╇━━━━━╇━━━━╇━━━━╇━━━━╇━━━━━┩\n│ D# │ F  │ F#  │ G# │ A# │ B  │ C#  │\n└────┴────┴─────┴────┴────┴────┴─────┘\n\n```\n\n\n## Acordes\n\nUso básico\n\n```bash\nnotas-musicais acorde\n┏━━━┳━━━━━┳━━━┓\n┃ I ┃ III ┃ V ┃\n┡━━━╇━━━━━╇━━━┩\n│ C │ E   │ G │\n└───┴─────┴───┘\n```\n\n### Variações na cifra\n\n```bash\nnotas-musicais acorde C+\n┏━━━┳━━━━━┳━━━━┓\n┃ I ┃ III ┃ V+ ┃\n┡━━━╇━━━━━╇━━━━┩\n│ C │ E   │ G# │\n└───┴─────┴────┘\n```\n\nAté o momento você usar acordes maiores, menores, dimunito e aumentados\n\n\n## Campo harmônico\n\nVocê pode chamar os campos harmônicos via o subcomando `campo-harmonico`. Por exemplo:\n\n```bash\nnotas-musicais campo-harmonico\n\n┏━━━┳━━━━┳━━━━━┳━━━━┳━━━┳━━━━┳━━━━━━┓\n┃ I ┃ ii ┃ iii ┃ IV ┃ V ┃ vi ┃ vii° ┃\n┡━━━╇━━━━╇━━━━━╇━━━━╇━━━╇━━━━╇━━━━━━┩\n│ C │ Dm │ Em  │ F  │ G │ Am │ B°   │\n└───┴────┴─────┴────┴───┴────┴──────┘\n```\n\nPor padrão os parâmetros utilizados são a tônica de `C` e o campo harmônico `maior`.\n\n### Alterações nos campos harmônicos\n\nVocê pode alterar os parâmetros da tônica e da tonalidade.\n\n```bash\nnotas-musicais campo-harmonico [TONICA] [TONALIDADE]\n```\n\n#### Alteração na tônica do campo\n\nUm exemplo com o campo harmônico de `E`:\n\n```bash\nnotas-musicais campo-harmonico E\n\n┏━━━┳━━━━━┳━━━━━┳━━━━┳━━━┳━━━━━┳━━━━━━┓\n┃ I ┃ ii  ┃ iii ┃ IV ┃ V ┃ vi  ┃ vii° ┃\n┡━━━╇━━━━━╇━━━━━╇━━━━╇━━━╇━━━━━╇━━━━━━┩\n│ E │ F#m │ G#m │ A  │ B │ C#m │ D#°  │\n└───┴─────┴─────┴────┴───┴─────┴──────┘\n```\n\n#### Alteração da tonalidade do campo\n\nUm exemplo utilizando o campo harmônico de `E` na tonalidade `menor`:\n\n```bash\nnotas-musicais campo-harmonico E menor\n\n┏━━━━┳━━━━━┳━━━━━┳━━━━┳━━━━┳━━━━┳━━━━━┓\n┃ i  ┃ ii° ┃ III ┃ iv ┃ v  ┃ VI ┃ VII ┃\n┡━━━━╇━━━━━╇━━━━━╇━━━━╇━━━━╇━━━━╇━━━━━┩\n│ Em │ F#° │ G   │ Am │ Bm │ C  │ D   │\n└────┴─────┴─────┴────┴────┴────┴─────┘\n```\n\n## Mais informações sobre o CLI\n\nPara descobrir outras opções, você pode usar a flag `--help`:\n\n```bash\nnotas-musicais --help\n                                                                       \n Usage: notas-musicais [OPTIONS] COMMAND [ARGS]...\n\n╭─ Commands ──────────────────────────────────────────────────────────╮\n│ acorde                                                              │\n│ campo-harmonico                                                     │\n│ escala                                                              │\n╰─────────────────────────────────────────────────────────────────────╯\n```\n\n### Mais informações sobre os subcomandos\n\nAs informações sobre os subcomandos podem ser acessadas usando a flag `--help` após o nome do parâmetro. Um exemplo do uso do `help` nos campos harmônicos:\n\n```bash\nnotas-musicais campo-harmonico --help\n                                                                       \n Usage: notas-musicais campo-harmonico [OPTIONS] [TONICA] [TONALIDADE] \n                                                                       \n╭─ Arguments ─────────────────────────────────────────────────────────╮\n│   tonica          [TONICA]      Tônica do campo harmônico           │\n│                                 [default: c]                        │\n│   tonalidade      [TONALIDADE]  Tonalidade do campo harmônico       │\n│                                 [default: maior]                    │\n╰─────────────────────────────────────────────────────────────────────╯\n╭─ Options ───────────────────────────────────────────────────────────╮\n│ --help          Show this message and exit.                         │\n╰─────────────────────────────────────────────────────────────────────╯\n```\n',
    'author': 'dunossauro',
    'author_email': 'mendesxeduardo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
