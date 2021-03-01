# Wojskowa komisja uzupełnień. Prawie.
Created for teachers. Not by teachers.

## Instalacja

1. Zainstauj `Python`.
2. Wpisz w CMD `pip install django`
3. Otwórz `startup.bat` w trybie edycji, a następnie zmień ścieżkę do twojej aplikacji na komputerze.
4. Zmień nazwę głównego folderu aplikacji, jeśli zajdzie taka potrzeba na `wku_django`.
5. Sprawdź czy `startup.bat` działa i hostuje aplikację.
6. Możesz stworzyć skrót do `startup.bat` i wrzucić sobie na pulpit.

## Opis

### Kompleks aplikacji wspierający nauczycieli w powtarzających się czynnościach.

Jeżeli wszystko poszło zgodnie z planem aplikacja będzie dostępna pod `127.0.0.1:8005/`.

#### Filler - automatyczne uzupełnianie obecności na dzienniku Vulcan.

Znajdziejsz go pod `/filler`. Aplikacja wymaga logowania. Jeżeli nie masz konta załóż je poprzez `/admin` logując się na wczesniej utworzonego `superusera`.

Dane logowania są bezpośrednio powiązane z aplikacją, więc upewnij się, że `email` oraz `hasło` zgadzają się z twoimi danymi do Vulcan.

Program służy do zautomatyzowania procesu wpisywania obecności uczniom na platformie Uonet Vulcan. Oferuje on wiele opcji oraz funkcji pod tym względem, między innymi równobieżne dbanie o porządek plików z Teams, poprzez tworzenie kopii tych plików z unikatowymi nazwami pod folderem, który jest wskazany w ustawieniach jako `Archiwum`, zadbaj więc o to, aby pliki te były zapisywane w wskazanym przez Ciebie miejscu.
> Uwaga. Ścieżka powinna być ścieżką absolutną. Pozwala to na jednoznaczne określenie miejsca archiwum w systemie, jednocześnie nie zwracając uwagi, gdzie znajduje się aktualnie aplikacja.

Lista obecności uzupełniana jest na podstawie pliku pobranego z Teams ( lub też nie ). W przypadku przekazania pliku na końcu program wygeneruje listę stworzoną na podstawie tego pliku na stronie Vulcan, w celu sprawdzenia czy aplikacja poprawnie wykonała swoją pracę.

Aplikacja udostępnia także opcje związane z na przykład dwoma lekcjami pod rząd, wpisaniu wszystkim uczniom jednakowych obecności ( jeżeli plik nie został przekazany ), wybór lekcji, instytucji czy ustawienie statusu nieobecnego ucznia innego niż `nieobecny`.


## Problemy z aplikacją
### ModuleNotFound
W CMD na ścieżcie głównego folderu aplikacji spróbuj wywołać `.\venv\Scripts\activate`. Jeżeli w CMD nie pojawi się `(venv)` przed poleceniem oznacza to, że powinnieneś sprawdzić kompletność aplikacji lub spróbować pobrać z `PyPI` dependencję `venv`.
W przypadku powodzenia wpisz `pip install -r requirements.txt`. Zainstaluje to wszystkie zdefiniowane dependencje projektowe zapisane w pliku `requirements.txt`.
