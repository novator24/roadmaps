Write-Host "Сборка LaTeX файла portfolio.tex..." -ForegroundColor Cyan
pdflatex portfolio.tex
Write-Host "Повторная сборка для генерации оглавления..." -ForegroundColor Cyan
pdflatex portfolio.tex

if (Test-Path "portfolio.pdf") {
    Rename-Item -Path "portfolio.pdf" -NewName "PORTFOLIO.pdf" -Force
    Write-Host "Сборка успешно завершена! Файл PORTFOLIO.pdf создан." -ForegroundColor Green
} else {
    Write-Host "Ошибка при сборке PDF. Убедитесь, что установлен дистрибутив LaTeX (например, MiKTeX или TeX Live)." -ForegroundColor Red
}