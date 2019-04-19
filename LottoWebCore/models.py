from django.db import models

from LottoWebCore.methods import create_hash


class City(models.Model):
    name = models.CharField(max_length=500, verbose_name='Cidade', unique=True, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"


class University(models.Model):
    name = models.CharField(max_length=500, verbose_name='Universidade', unique=True)
    page = models.CharField(max_length=500, verbose_name='Website')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Universidade"
        verbose_name_plural = "Universidades"


class StudentDirectory(models.Model):
    name = models.CharField(max_length=500, null=False, verbose_name='Nome do Centro')
    phone = models.CharField(max_length=500, null=False, verbose_name='Telefone ou Ramal')
    email = models.CharField(max_length=500, null=False, verbose_name='E-mail')
    room = models.CharField(max_length=500, verbose_name='Sala')
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False, verbose_name='Cidade')
    university = models.ForeignKey(University, on_delete=models.CASCADE, null=False, verbose_name='Universidade')

    class Meta:
        unique_together = ("name", "university", "city")
        verbose_name = "Centro Acadêmico"
        verbose_name_plural = "Centros Acadêmicos"

    def __str__(self):
        return self.name


class Raffle(models.Model):
    name = models.CharField(max_length=500, verbose_name='Nome do Sorteio')
    phone = models.CharField(max_length=500, verbose_name='Telefone do Responsável')
    email = models.CharField(max_length=500, verbose_name='E-mail')
    completed = models.BooleanField(default=False, verbose_name="Finalizado")
    creation = models.DateTimeField(auto_now_add=True)
    lottery = models.DateTimeField(null=True, verbose_name="Data do Sorteio")
    id = models.CharField(max_length=10, default=create_hash, unique=True, primary_key=True)
    directory = models.ForeignKey(StudentDirectory, on_delete=models.CASCADE, verbose_name='Centro Acadêmico')

    readonly_fields = ('id',)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sorteio"
        verbose_name_plural = "Sorteios"


class MiddleMan(models.Model):
    analysed = models.BooleanField(default=False)
    name = models.CharField(max_length=500, null=False)
    phone = models.CharField(max_length=500, null=False)
    email = models.CharField(max_length=500, null=False)
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)
    id = models.CharField(max_length=10, default=create_hash, unique=True, primary_key=True)
    directory = models.ForeignKey(StudentDirectory, on_delete=models.CASCADE)

    readonly_fields = ('id',)

    class Meta:
        unique_together = ["name", "directory", "id", "raffle"]
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"

    def __str__(self):
        return self.name


class Ticket(models.Model):
    name = models.CharField(max_length=500, verbose_name='Comprador')
    phone = models.CharField(max_length=500, verbose_name='Telefone')
    email = models.CharField(max_length=500, verbose_name='E-mail')
    verified = models.BooleanField(default=False)  # by the Student Directory
    notified = models.BooleanField(default=False)  # by the SERVER and to the client
    activated = models.BooleanField(default=False)  # by LABAM
    created = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(MiddleMan, on_delete=models.CASCADE, verbose_name='Vendedor')
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE, verbose_name='Rifa')
    id = models.CharField(max_length=10, default=create_hash, unique=True, primary_key=True)
    directory = models.ForeignKey(StudentDirectory, on_delete=models.CASCADE, verbose_name='Centro Acadêmico')

    readonly_fields = ('id',)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = "Bilhete"
        verbose_name_plural = "Bilhetes"


class RegistrationRequest(models.Model):
    name = models.CharField(max_length=500, null=False)
    email = models.CharField(max_length=500, null=False, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Solicitação de Registro"
        verbose_name_plural = "Solicitações de Registro"
