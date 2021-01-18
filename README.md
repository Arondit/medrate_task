# medrate_task

Основной текст представлен в файле review.pdf. Далее краткое описание подхода к написанию программы:

Основной файл с кодом, script.py, построен таким образом, чтобы его можно было использовать, как библиотечный код. Несмотря на усложнение кода в самом файле, так его гораздо проще использовать в другом скрипте.

Функция main принимает в качестве необязательных параметров функцию получения данных и функцию обработки данных, а также два булевых значения: проводить ли проверку корректности последнего завершения программы, и показывать ли время выполнения скрипта. Поэтому для переопределения способа обработки данных не нужно переписывать функцию в исходном файле, достаточно использовать в другом файле любую стороннюю функцию.

Это реализовано в файле parallel.py, в котором просто переопределена функция параллельной обработки данных, и для этого понадобилось только импортировать функцию транзакции и саму функцию main.

Код выделен в функции по смысловому принципу, чтобы между разными действиями было легко что-то добавить, или чтобы можно было их подменить. Для более вариативной задачи можно легко преобразовать этот код в паттерн «Шаблонный метод».

Программа проверялась на Ubuntu 18.04. 
