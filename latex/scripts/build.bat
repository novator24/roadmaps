@echo off
echo Сборка LaTeX файла portfolio.tex...
pdflatex portfolio.tex
echo Повторная сборка для генерации оглавления...
pdflatex portfolio.tex
if exist portfolio.pdf (
    move /Y portfolio.pdf PORTFOLIO.pdf
    echo Сборка успешно завершена! Файл PORTFOLIO.pdf создан.
) else (
    echo Ошибка при сборке PDF. Убедитесь, что установлен дистрибутив LaTeX (например, MiKTeX или TeX Live).
)
pause