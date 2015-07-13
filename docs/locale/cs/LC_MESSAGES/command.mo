��    @                            5  l   N  >   �  6   �  ^   1  C   �  	  �  ?   �  .        M  8   Y     �     �  x   �          ,     ?     X     q  V   �     �     �  @   	      C	     d	  6   �	  @   �	  c   �	     ^
     }
     �
     �
     �
  !   �
     �
  C     "   U     x     �  <   �  ?   �  j   /     �     �  K   �  P     L   ]     �     �     �     �     �  0      V   1  �   �  A      �   b  �   �     m  p   �  C   �  o   :  �  �     �     �  m   �  @   *  9   k  [   �  Z       \  8   e  3   �     �  <   �  
           �   (     �     �  '   �  !        '  W   8     �      �  8   �  -     )   4  4   ^  2   �  {   �     B     Y     v     �     �  +   �     �  E     '   G     o  "   �  ;   �  ?   �  o   -     �     �  R   �  T     Y   n     �      �       	     	   #  K   -  ^   y  �   �  H   �  �   �  s   \       �   �   �   S   �!  �   �!   :file:`/etc/xdg/odorik` :file:`~/.config/odorik` API password. Use API password for per user access and line password (used for SIP as well) for line access. API server URL, defaults to ``https://www.odorik.cz/api/v1/``. API user, can be either ID registered user or line ID. Additional parameters can be specified by ``--param`` switch which can be used multiple times. Additionally config file can include phone number and line aliases: All parameters accepting date can take almost any format of date or timestamp. Check `dateutil <http://labix.org/python-dateutil#head-b95ce2094d189a89f80f5ae52a05b4ab7b41af47>`_ documentation for more detailed information (especially on year/month/day precendence). Commands actually indicate which operation should be performed. Currently following subcommands are available: Description Ending datetime. If not specified, current date is used. Examples Files Following settings can be configured in the ``[odorik]`` section (you can customize this by :option:`--config-section`): Generic API POST: Generic API usage: Getting account summary: Global configration file Global options If ``--all`` is specified, summary for all mobile lines on current account is printed. Initiates a callback. Initiating callback: It can list all individual records when ``--list`` is specified. Machine readable output formats: Odorik command line interface Override path to configuration file, see :ref:`files`. Override section to use in configuration file, see :ref:`files`. Performs authenticated API call. By default ``GET`` method is used, with ``--post`` it is ``POST``. Print current program version: Print current user balance: Prints SMS usage. Prints calls usage. Prints current balance. Prints current mobile data usage: Prints current version. Prints information for current month. This is the default interval. Prints information for last month. Prints infromation about lines. Prints mobile data usage. Prints summary information for all lines in current account. See :ref:`interval` for information how to specify date period. See `Autentizace Odorik API <http://www.odorik.cz/w/api#autentizace>`_ for more details on authentication. Sending message: Sends a SMS message. Specify API URL. Overrides value from configuration file, see :ref:`files`. Specify API password. Overrides value from configuration file, see :ref:`files`. Specify API user. Overrides value from configuration file, see :ref:`files`. Specify output format. Specifying date period Starting datetime. Subcommands Synopsis The configuration file is INI file, for example: The program accepts following global options, which must be entered before subcommand. The program follows XDG specification, so you can adjust placement of config files by environment variables ``XDG_CONFIG_HOME`` or ``XDG_CONFIG_DIRS``. The result can be also limited to given line by using ``--line``. The result can be also limited to given phone number by using ``--phone``. The phone number has to be specified as ``00420789123456``. This module also installs :program:`odorik` program, which allows you to easily access some of the functionality from command line. User configuration file With ``--generate-config`` it generates config file entries for line and phone number aliases, see :ref:`files`. You can specify date period for which many commands will be issued: You can specify sender number by ``--sender``, it has to be one of allowed values. By default ``5517`` is used. Project-Id-Version: Odorik 0.5
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2015-05-20 15:07+0200
PO-Revision-Date: 2015-05-20 16:33+0200
Last-Translator: Michal Čihař <michal@cihar.com>
Language-Team: Czech <https://hosted.weblate.org/projects/odorik/documentation-command/cs/>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Language: cs
Plural-Forms: nplurals=3; plural=(n==1) ? 0 : (n>=2 && n<=4) ? 1 : 2;
X-Generator: Weblate 2.3-dev
 :file:`/etc/xdg/odorik` :file:`~/.config/odorik` API heslo. Použijte API heslo pro uživatele nebo heslo linky (stejné jako pro SIP) pro přístup na linku. URL API serveru, výchozí je ``https://www.odorik.cz/api/v1/``. API uživatel, může být buď ID uživatele nebo linky. Další parametry můžete zadat volbou ``--param``, která může být uvedena vícekrát. Dále může konfigurační soubor obsahovat pojmenování pro telefonní čísla a linky: Všechny volby zpracují datum nebo čas v téměř jakémkoliv formátu. V dokumentaci k `dateutil <http://labix.org/python-dateutil#head-b95ce2094d189a89f80f5ae52a05b4ab7b41af47>`_ naleznete podrobnější popis (obzvlášť popis pořadí roku, měsíce a dne). Jednotlivé příkazy určují jaká operace se provede. V současné době jsou k dispozici tyto příkazy: Popis Koncové datum. Pokud nebude zadáno použije se aktuální. Příklady Soubory Následující parametry mohou být nastaveny v sekci ``[odorik]`` (nebo vámi zadané pomocí volby :option:`--config-section`): Obecné použití POST API: Obecné použití API: Výpis souhrnných informací o účtu: Systémový konfigurační soubor Globální volby Pokud použijete volbu ``--all``, program vypíše souhrn pro všechny linky na účtu. Objedná zpětné volání. Objednání zpětného volání: S parametrem ``--list`` vypíše i jednotlivé položky. Strojově zpracovatelné výstupní formáty: Rozhraní Odorik pro příkazovou řádku Cesta ke konfiguračnímu souboru, viz :ref:`files`. Sekce v konfiguračním souboru, viz :ref:`files`. Provede autentizované volání API. Jako výchozí se použije metoda ``GET``, volbou ``--post`` ji změníte na ``POST``. Vypsat verzi programu: Vypsat aktuální zůstatek: Vypíše SMS zprávy. Vypíše hovory. Vypíše aktuální zůstatek. Vypsat aktuální využití mobilních dat: Vypíše verzi programu. Vypíše informace pro tento měsíc. Jedná se o výchozí interval. Vypíše informace pro minulý měsíc. Vypíše informace o linkách. Vypíše použití mobilních dat. Vypíše souhrnné informace o všech linkách pod účtem. Informace o zadání intervalu dat naleznete v :ref:`interval`. Více informací naleznete na wiki v sekci  `Autentizace Odorik API <http://www.odorik.cz/w/api#autentizace>`_. Odeslání zprávy: Odešle SMS zprávu. Nastaví API URL. Přepíše hodnotu z konfiguračního souboru, viz :ref:`files`. Nastaví API heslo. Přepíše hodnotu z konfiguračního souboru, viz :ref:`files`. Nastaví API uživatele. Přepíše hodnotu z konfiguračního souboru, viz :ref:`files`. Určí výstupní formát. Zadávání časového intervalu Počáteční datum. Příkazy Použití Konfigurační soubor je ve formátu INI. Například může vypadat takto: Program rozumí následujícím globálním volbám. Tyto musí být zadány před příkazem. Program dodržuje specifikaci XDG, takže umístění konfiguračních souborů můžete ovlivnit proměnnými prostředí  ``XDG_CONFIG_HOME`` nebo ``XDG_CONFIG_DIRS``. Výsledek může být také omezen na jednu linku použitím ``--line``. Výsledek může být také omezen na telefonní číslo zadáním volby ``--phone``. Telefonní číslo zadávejte ve tvaru ``00420789123456``. Tento modul také nainstaluje program :program:`odorik`, který vám ho umožní používat z příkazové řádky. Konfigurační soubor uživatele S volbou ``--generate-config`` tento příkaz vytvoří položky do konfiguračního souboru pro pojmenování linek a telefonních čísel, viz :ref:`files`. Pro mnoho příkazů můžete zadat časový interval na který se budou aplikovat: Číslo odesílatele můžete změnit pomocí ``--sender``. Musí se jednat o jednu z povolených hodnot. Jako výchozí se použije ``5517``. 