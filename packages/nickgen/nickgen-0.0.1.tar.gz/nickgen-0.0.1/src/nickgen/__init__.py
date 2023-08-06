from nickgen.login_macros_handler import LoginMacrossHandler


def generate(template="[Eng|4][RndNum|1970|1990]") -> str:
    """[Eng|4][RndNum|1970|1990]\n
    [Jap|4][RndNum|1970|1990]\n
    [Lat|4][RndNum|1970|1990]\n

    На данный момент поддерживаются языки Eng - английский, Lat - латынь, Jap - японский.
    То есть написав [Eng|4], будет сгенерирован никнейм длиной в 4 английских слога, с вероятностью следования слогов такой же как в реальных словах. Поигравшись с формулой генерации, можно создать более сложные конструкции:
    [RndSym|[RndNum|0|4]|0123456789][Lat|3][RndSym|[RndNum|0|2]|-][Jap|1][RndText|2|D]
    где [RndSym|[RndNum|0|4]|0123456789] - в начале ника идет от 0 до трех цифр;
    [Lat|3] 3 слога на латыни;
    [RndSym|[RndNum|0|2]|-] возможно появление дефиса;
    [Jap|1] один японский слог;
    [RndText|2|D] потом случайные 2 буквы или цифры;

    В результате будут сгенерированы ники:
        053bomenca-iem\n
        7lialeme-nozr\n
        46atbemig-poex\n
        simpvido-se8f\n
        3afosuxhif6\n
        frigulimdeif\n
        misssefu-yucn\n
        5grasacin-maew\n
        trodalcelfu88\n
        6nasercia-risc

    Args:
        template (str, optional): _description_. Defaults to '[Eng|4][RndNum|1970|1990]'.

    Returns:
        str: _description_
    """
    return LoginMacrossHandler.GetLogins(template, 1)[0]


def generate_many(count=1, template="[Eng|4][RndNum|1970|1990]") -> tuple[str]:
    """Смотри описание метода generate()

    Args:
        count (int, optional): Amount logins. Defaults to 1.
        template (str, optional): Generation template. Defaults to '[Eng|4][RndNum|1970|1990]'.

    Returns:
        tuple[str]: _description_
    """
    return LoginMacrossHandler.GetLogins(template, count)
