# SZE-FordProg-2020-BoolAlgebra-2
Hollosy Adam

Boolean Kalkulátor

Ebben a kis Python programban egy végtelenül egyszerű, boolean kifejezéseket kiértékelő kalkulátor
megvalósítását tűztem ki célul. Nyilván, a projekt elsődleges célja, hogy a Ply lex és yacc Python
implementációjának használatában mélyedjek kicsit el, így bár a képességei igencsak limitáltak,
viszont a Ply elemeivel való ismerkedés jól mutatja, milyen hatékony eszköz lehet egy nagyobb
projektben használva, amennyiben tokenizálásra és parse-olásra lenne szükség.

A fő funkciók bemutatása:

A kalkulátor az elindítása után egy promptot jelenít meg, és várja a felhasználótól, hogy
adjon meg szintaktikailag helyes logikai kifejezéseket, mellyel a továbbiakban dolgozni tud. A program lehetőséget biztosít a maga szerény módján "változók bevezetésére" is. Ezeket egy
értékadás művelettel tudjuk deklarálni és definiálni is egyben. A változók tartalma tetszőleges alkalommal megváltoztatható egy rajtuk elvégzett újabb értékadással, illetve tartalmuk bármikor lekérdezhető. A helytelen változónevekről, illetve a szintaktikailag hibás kifejezésekről adekvát hibaüzenetekben kapunk tájékoztatást.

A logikai kifejezések a következő építőkockákból állnak:

  - A legalapvetőbb, két db logikai literál, az 1 (igaz) és a 0 (hamis). A program jelenleg ezt a két karaktert tekinti csak valid literálnak. Ez azért van, mert bár lehetett volna még a különböző string reprezentációkat is figyelembe venni összetettebb regexpek segítségével, de akkor túlságosan bonyolulttá vált volna a tokenkezelés. Jelenleg a feldolgozás során minden 0 = hamis, minden (1 és annál nagyobb számjegy) = igaznak értékelődik ki; ez nem jelent a működésre nézve további fennakadásokat, de a konvertálási technikából származó tulajdonságként mindenképpen megemlítendő.
  
- Az implementált logikai operátorok: AND (and, &&), OR (or, ||), XOR (xor, ^), NOT (not, !)
Mint látható, itt már a program képes felismerni a csak nagybetűs, csak kisbetűs, illetve a speciális karakterükkel megadott operátorokat is.

- Változók és azok bevezetése; a következő egyszerű módon tudunk deklarálni és definiálni változókat:
v_a = 1 vagy vb23 = 0, illetve v_logikai_literal = 1.
Minden változó neve kötelezően kis v betűvel kell hogy kezdődjön, majd minimum egy (de tetszőleges számú) kisbetű, nagybetű, szám, illetve alahúzasjel konkatenációja által alkotta string következhet.
Ha helytelen változót próbálunk bevezetni, arról hibaüzenetet fogunk kapni.
Hibás névkonvenció például: rossz_valtozonev=1

Most, hogy az alapvető építőkockákat megismertük, nézzünk példákat sorban a fentiek használatára.
Vizsgáljuk meg a következő kifejezéseket, milyen eredményt kapunk:


BoolCalc>>> 1 AND 1

('AND', True, True)

True


Jelmagyarázat, az egyes sorok részletes jelentésére:
- Az első sorban áll az általunk bevitt kifejezés.
- A második sorban azt láthatjuk, milyen szintaxis-fa felépülését eredményezi a bevitt kifejezés.
Jelen esetben két igaz literál között teremtettünk ÉS kapcsolatot.
- A harmadik sor szolgáltatja az egész kifejezés kiértékelése után előálló végeredményt.
Ebben az esetben ennek értéke IGAZ.

Ha csak egy literált vizsgálunk önmagában, mint logikai kifejezést, természetesen annak a "szintaxis-fája" és eredménye is saját maga lesz:


BoolCalc>>> 1

True

True


BoolCalc>>> 0

False

False


A szintaxis-fa generáló működés lehetővé teszi, hogy tetszőlegesen összetett kifejezéseket kombináljunk egymással, és ezeket vizsgáljuk:


BoolCalc>>> 1 AND 0 OR 1 AND NOT 0

('OR', ('AND', True, False), ('AND', True, True))

True


A fenti kifejezés értéke mint láthatjuk IGAZ. Itt azonban előjön a logikai operátorok közötti
precedencia kérdése, melyet a program képes az általunk meghatározott, előírt sorrend szerint kezelni.
Jelen esetben az ÉS operátorok által elvégzett műveletek kiértékelése után következik a VAGY operátor
végrehajtása. Ez a viselkedés helyes, hiszen mint azt a kódban láthatjuk is, a logikai operátorok precedenciáját a következő sorrendben határoztuk meg:
NOT > AND > XOR > OR.

Nézzünk példákat bonyolultabb kifejezésekre, ahol már fölváltva használjuk a különböző logikai operátorok eltérő reprezentációit:


BoolCalc>>> NOT NOT NOT 1

False

False


BoolCalc>>> 1 or 0 XOR not 0 AND 0

('XOR', ('or', True, False), ('AND', True, False))

True


BoolCalc>>> 0 XOR 1 or 1 and NOT not 0 && 1 or !1 ^ 0 || 1

('||', ('^', ('or', ('or', ('XOR', False, True), ('&&', ('and', True, False), True)), False), False), True)

True


Mint láthatjuk, ez sem okoz problémát a kiértékelésben. A következőkben próbáljunk meg szintaktikailag szándékosan hibás kifejezést megadni:


BoolCalc>>> 1 OR 1 AND AND 1

Szintaxis hiba a bemeneten!

True

True


A fentiek esetén a két egymást követő ÉS operátort természetesen szintaktikai hibának érzékelte a program. Ilyen esetben mint látjuk, a szintaktikailag helyes, "maradék" tokenekből bár megpróbál előállítani bizonyos eredményt; viszont ez az eredmény, a "maradék volta" miatt szemantikailag már aggályos, nem éri meg belőle az eredeti kifejezésre nézve messzemenő következtetéseket levonni :)

Lássunk példát változó bevezetésére, majd annak értékének lekérdezésére:


BoolCalc>>> v_a = 1

('=', 'v_a', True)


A már inicizalizált változó értéke bármikor felülírható az értékadó kifejezés megismétlésével, azt a már létező változón újra elvégezve. Illetve, az adott változó tartalmát bármikor le is kérdezhetjük:


BoolCalc>>> v_a

('valtozo', 'v_a')

True


Próba helytelen változó bevezetésére, illetve kísérlet nem létező (bár névkonveció szempontjából helyes) változó lekérdezése:


BoolCalc>>> abcd=0

Nem megengedett karakter erkezett a bemeneten!

Nem megengedett karakter erkezett a bemeneten!

Nem megengedett karakter erkezett a bemeneten!

Nem megengedett karakter erkezett a bemeneten!

Szintaxis hiba a bemeneten!

False

False



BoolCalc>>> v_helyesen_elnevezett_de_nem_letezo_valtozo  

('valtozo', 'v_helyesen_elnevezett_de_nem_letezo_valtozo')

Nem definialt valtozo!



Végül, nézzük meg a már definiált értékkel bíró változók használatát a logikai kifejezésekben:
- A példában használt változók értéke: v_var1=1, v_varC=0, v_var_005=1


BoolCalc>>> NOT 1 OR v_var1 AND v_varC XOR v_var005

('XOR', ('OR', False, ('AND', ('valtozo', 'v_var1'), ('valtozo', 'v_varC'))), ('valtozo', 'v_var005'))

True


Mint láthatjuk, a változók tárolt értéke behelyettesítődik a kiértékelés előtt, majd a helyes eredményt kapjuk.

A program létrehozásában segítésgemre voltak a következő források:

- PLY (Python Lex-Yacc) David M. Beazley - https://www.dabeaz.com/ply/ply.html
- Make your Own Calculator in Python - https://youtu.be/Hh49BXmHxX8





---------------------------
!!KNOWN ISSUE: Az igazsághoz hozzá tartozik, hogy egy bizonyos esetben hibás működést figyeltem meg,
amit még nem sikerült kiküszöbölnöm, további utángondolást igényel a megoldása. A változók negálásánál, amennyiben annak értéke HAMIS, sajnos nem történik meg a negáció (valószínű, hogy az IGAZ értéknél is falshelyes hamis eredményértékkel van dolgom). Tehát a NOT v_var_005 esetén fals hamis érték jelentkezik.











