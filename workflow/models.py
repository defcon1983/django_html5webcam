from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator



# Create your models here.
DVOM_LOCATIES = (
    ('NL', 'Nederland'),
    ('BE', 'Belgie'),
)

DVOM_CLASSIFICATIE_OPTIES = (
    ('FR', 'Fraude'),
    ('JE', 'Jeugd'),
    ('MH', 'Mensenhandel'),
    ('MI', 'Militair'),
    ('TR', 'Terrorisme'),
)
DVOM_AFSLUITENONDERZOEK_OPTIES = (
    ('1', 'Er is geen verdachte'),
    ('2', 'Klappen zaak - de verdacht wordt vervolgd'),
    ('3', 'Sepot'),
)

class Onderzoek(models.Model):
    dvom_onderzoekid = models.AutoField(primary_key=True)
    dvom_locatieid = models.CharField('Parket', max_length=10, choices=DVOM_LOCATIES, default='')
    dvom_naam = models.CharField('Onderzoeksnaam', max_length=100, blank=True, null=True)
    dvom_codenaam = models.CharField('Codenaam', max_length=100, blank=True, null=True)
    dvom_onderzoeksinstantieid = models.CharField('Onderzozeksinstantie', max_length=10,  choices=())
    dvom_procesverbaalnummer = models.CharField('Process verbaal nummer',max_length=100, )
    dvom_classificatie = models.CharField('Classificatie', max_length=2, choices=DVOM_CLASSIFICATIE_OPTIES, blank=True, null=True)
    dvom_naamcsv = models.CharField('Naam CSV', max_length=100, blank=True, null=True)
    dvom_omschrijvingcsv = models.CharField('Omschrijving CSV', max_length=2000, blank=True, null=True)
    dvom_zaakgriffierid = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Zaaksgriffier',
                                            related_name='zaakgriffier_onderzoeken', null=True)
    dvom_zaakovjid = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='ZaaksOvJ',
                                       related_name='zaakovj_onderzoeken', null=True)
    dvom_zaakparketsecrid = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Zaakssecretaris',
                                              related_name='zaakparketsecr_onderzoeken', null=True)
    dvom_zaakrcid = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='ZaaksRC',
                                      related_name='zaakrc_onderzoeken', null=True)
    dvom_afsluitenonderzoek = models.CharField('Afsluiten onderzoek',
                                               max_length=1,
                                               choices=DVOM_AFSLUITENONDERZOEK_OPTIES, blank=True, null=True)
    np_bobaanvraagid = models.IntegerField()

    class Meta:
        ordering = ['-dvom_onderzoekid']
        verbose_name_plural = 'Onderzoeken'

    def __str__(self):
        return f"{self.dvom_naam} - {self.dvom_codenaam}"

    def get_absolute_url(self):
        return reverse('onderzoek-detail', args=[str(self.dvom_onderzoekid)])



ONDERZOEK_TYPES = (
    ('SO', 'Strafrechtelijk Onderzoek'),
    ('SF', 'Strafrechtelijk Financieel Onderzoek'),
    ('SE', 'Strafrechtelijk Executie Onderzoek'),
)

BOOL_CHOICES = ((True, 'Ja'), (False, 'Nee'))

VERLENING_PERIODES = (
    ('DD', 'Dag/Dagen'),
    ('WW', 'Week/Weken'),
    ('MM', 'Maand/Maanden'),
)




def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    #return 'user_{0}/{1}'.format(instance.user.id, filename)
    return 'user_{0}/{1}'.format(instance.user.username, filename)


class BOBAanvraag(models.Model):
    dvom_bobhandelingid = models.AutoField(primary_key=True)
    dvom_bobhandeling = models.CharField('BOB handeling', max_length=100, help_text='Naam van de bob handeling')
    dvom_aanvraagpv = models.CharField('Aanvraag PV', max_length=50)
    dvom_datumpv = models.DateField()
    dvom_verbalisant  = models.CharField('Naam verbalisant', max_length=100, help_text='Naam van de verbalisant')
    dvom_verbalisantcontactgegevens = models.EmailField(verbose_name='E-mail verbalisant',
                                                        help_text='Contactgegevens van de verbalisant')

    dvom_strafvorderlijkebevoegdheidid = models.CharField('Bevoegdheid', max_length=100, default='', help_text="""ID van de 
                                                          bevoegdheid """)

    dvom_verlenging = models.BooleanField(choices=BOOL_CHOICES, verbose_name='Verlenging', default=False)
    dvom_verlengingingaandop = models.DateField()
    dvom_verlengingeinddatum = models.DateField()
    dvom_verlengingnr = models.PositiveIntegerField('Verlenging nr', default=0, blank=True, null=True,
                                                    validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                    help_text='Hoeveelste verlenging betreft het'
                                                    )
    # Vordering tot machtiging
    dvom_vtmstartdatum = models.DateField(verbose_name='VTMStartdatum / Op')
    dvom_vtmeinddatum = models.DateField(verbose_name='VTMEinddatum')

    dvom_periode_aantal = models.PositiveIntegerField('Aantal (periode)', default=0,
                                                         validators=[MinValueValidator(1), MaxValueValidator(100)],
                                                         help_text="""Periode vordering tot machtiging  
                                             (aantal i.c.m.volgend veld)""")

    dvom_periode_periode = models.CharField('Periode (eenheid)', max_length=2, choices=VERLENING_PERIODES,
                                               help_text="""Eenheid van de periode tot vordering tot machtiging  
                                           """)

    # Machtiging fields

    pdf_document = models.FileField('PDF Document', upload_to='documents/%Y/%m/%d', blank=True, null=True)


    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    def __str__(self):
        return f"{self.dvom_bobhandeling} (#{self.dvom_bobhandelingid}) - PV: {self.dvom_aanvraagpv} "

    def get_absolute_url(self):
        return reverse('bobhandeling-detail', args=[str(self.dvom_bobhandelingid)])

    def clean(self):
        print("BobHandeling::clean()...")
        self.dvom_bobhandeling = '_'.join(["BOB_handeling", self.dvom_aanvraagpv, str(self.dvom_datumpv)])
        print(f"self.dvom_bobhandeling: {self.dvom_bobhandeling}")
