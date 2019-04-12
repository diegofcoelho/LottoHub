from django.db import models


class University(models.Model):
    phd = models.IntegerField(default=0)
    master = models.IntegerField(default=0)
    name = models.CharField(max_length=500)
    page = models.CharField(max_length=500)
    teachers = models.IntegerField(default=0)
    employee = models.IntegerField(default=0)
    foundation = models.IntegerField(default=0)
    post_grads = models.IntegerField(default=0)
    undergrads = models.IntegerField(default=0)
    teachers_search = models.CharField(max_length=500)
    sigaa_home = models.CharField(max_length=500)


class Area(models.Model):
    name = models.CharField(max_length=500)


class Department(models.Model):
    name = models.CharField(max_length=500, null=False)
    city = models.CharField(max_length=500, null=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, null=False)
    select_value = models.IntegerField(default=0, unique=True)

    # area = models.ForeignKey(Area)

    class Meta:
        unique_together = (("name", "city", "university",),)


class Teacher(models.Model):
    cv = models.CharField(max_length=1000)
    name = models.CharField(max_length=500)
    room = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    registry = models.IntegerField(default=0)
    address = models.CharField(max_length=500)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    interest = models.CharField(max_length=1000)
    analysed = models.BooleanField(default=False)
    description = models.CharField(max_length=1000)

    class Meta:
        unique_together = ["name", "department"]


class Discipline(models.Model):
    name = models.CharField(max_length=500)
    code = models.CharField(max_length=500)
    workload = models.IntegerField(default=0)

    class Meta:
        unique_together = ["name", "code"]


class Lecture(models.Model):
    @property
    def code(self):
        return self.discipline.code

    @property
    def name(self):
        return self.discipline.name

    @property
    def workload(self):
        return self.discipline.workload

    tid = models.IntegerField(default=0)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    # name = models.CharField(max_length=500)
    term = models.CharField(max_length=500)
    # code = models.CharField(max_length=500)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    # workload = models.IntegerField(default=0)
    timetable = models.CharField(max_length=500)

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
        # unique_together = ["term", "code", "teacher"]
