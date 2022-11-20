# Generated by Django 4.0.4 on 2022-11-08 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_machine_translation_format'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine_translation',
            name='format',
            field=models.CharField(choices=[['afrikaans', 'afrikaans'], ['albanian', 'albanian'], ['amharic', 'amharic'], ['arabic', 'arabic'], ['armenian', 'armenian'], ['azerbaijani', 'azerbaijani'], ['basque', 'basque'], ['belarusian', 'belarusian'], ['bengali', 'bengali'], ['bosnian', 'bosnian'], ['bulgarian', 'bulgarian'], ['catalan', 'catalan'], ['cebuano', 'cebuano'], ['chichewa', 'chichewa'], ['chinese (simplified)', 'chinese (simplified)'], ['chinese (traditional)', 'chinese (traditional)'], ['corsican', 'corsican'], ['croatian', 'croatian'], ['czech', 'czech'], ['danish', 'danish'], ['dutch', 'dutch'], ['english', 'english'], ['esperanto', 'esperanto'], ['estonian', 'estonian'], ['filipino', 'filipino'], ['finnish', 'finnish'], ['french', 'french'], ['frisian', 'frisian'], ['galician', 'galician'], ['georgian', 'georgian'], ['german', 'german'], ['greek', 'greek'], ['gujarati', 'gujarati'], ['haitian creole', 'haitian creole'], ['hausa', 'hausa'], ['hawaiian', 'hawaiian'], ['hebrew', 'hebrew'], ['hebrew', 'hebrew'], ['hindi', 'hindi'], ['hmong', 'hmong'], ['hungarian', 'hungarian'], ['icelandic', 'icelandic'], ['igbo', 'igbo'], ['indonesian', 'indonesian'], ['irish', 'irish'], ['italian', 'italian'], ['japanese', 'japanese'], ['javanese', 'javanese'], ['kannada', 'kannada'], ['kazakh', 'kazakh'], ['khmer', 'khmer'], ['korean', 'korean'], ['kurdish (kurmanji)', 'kurdish (kurmanji)'], ['kyrgyz', 'kyrgyz'], ['lao', 'lao'], ['latin', 'latin'], ['latvian', 'latvian'], ['lithuanian', 'lithuanian'], ['luxembourgish', 'luxembourgish'], ['macedonian', 'macedonian'], ['malagasy', 'malagasy'], ['malay', 'malay'], ['malayalam', 'malayalam'], ['maltese', 'maltese'], ['maori', 'maori'], ['marathi', 'marathi'], ['mongolian', 'mongolian'], ['myanmar (burmese)', 'myanmar (burmese)'], ['nepali', 'nepali'], ['norwegian', 'norwegian'], ['odia', 'odia'], ['pashto', 'pashto'], ['persian', 'persian'], ['polish', 'polish'], ['portuguese', 'portuguese'], ['punjabi', 'punjabi'], ['romanian', 'romanian'], ['russian', 'russian'], ['samoan', 'samoan'], ['scots gaelic', 'scots gaelic'], ['serbian', 'serbian'], ['sesotho', 'sesotho'], ['shona', 'shona'], ['sindhi', 'sindhi'], ['sinhala', 'sinhala'], ['slovak', 'slovak'], ['slovenian', 'slovenian'], ['somali', 'somali'], ['spanish', 'spanish'], ['sundanese', 'sundanese'], ['swahili', 'swahili'], ['swedish', 'swedish'], ['tajik', 'tajik'], ['tamil', 'tamil'], ['telugu', 'telugu'], ['thai', 'thai'], ['turkish', 'turkish'], ['ukrainian', 'ukrainian'], ['urdu', 'urdu'], ['uyghur', 'uyghur'], ['uzbek', 'uzbek'], ['vietnamese', 'vietnamese'], ['welsh', 'welsh'], ['xhosa', 'xhosa'], ['yiddish', 'yiddish'], ['yoruba', 'yoruba'], ['zulu', 'zulu']], max_length=250),
        ),
    ]
