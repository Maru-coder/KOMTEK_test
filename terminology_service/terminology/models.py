from django.db import models


class Refbook(models.Model):
    code = models.CharField(max_length=100, unique=True, verbose_name="Код")
    name = models.CharField(max_length=300, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"

    def __str__(self):
        return self.name


class RefbookVersion(models.Model):
    refbook = models.ForeignKey(Refbook, on_delete=models.CASCADE, related_name='versions', verbose_name="Справочник")
    version = models.CharField(max_length=50, verbose_name="Версия")
    start_date = models.DateField(verbose_name="Дата начала версии")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['refbook', 'version'], name='unique_refbook_version'),
            models.UniqueConstraint(fields=['refbook', 'start_date'], name='unique_refbook_start_date'),
        ]
        verbose_name = "Версия справочника"
        verbose_name_plural = "Версии справочника"

    def __str__(self):
        return f"{self.refbook.name} - {self.version}"


class RefbookElement(models.Model):
    version = models.ForeignKey(RefbookVersion, on_delete=models.CASCADE, related_name='elements', verbose_name="Версия справочника")
    code = models.CharField(max_length=100, verbose_name="Код элемента")
    value = models.CharField(max_length=300, verbose_name="Значение элемента")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['version', 'code'], name='unique_version_code'),
        ]
        verbose_name = "Элемент справочника"
        verbose_name_plural = "Элементы справочника"

    def __str__(self):
        return f"{self.code} - {self.value}"
