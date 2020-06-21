# SZE-FordProg-2020-BoolAlgebra-2
Hollosy Adam

Boolean Kalkulátor

Ebben a kis python programban egy végtelenül egyszerű boolean kifejezéseket kiértékelő kalkulátor
megvalósítását tűztem ki célul. Nyilván a projekt elsődleges célja, hogy a Ply lex és yacc python
implementációjának használatában mélyedjek kicsit el, így a képességei igencsak limitáltak,
viszont a Ply elemeivel való ismerkedés jól mutatja, milyen hatékony eszköz lehet egy nagyobb
projektben használva, amennyiben tokenizálásra és parse-olásra lenne szükség.

A funkciók bemutatása:

A kalkulátor az elindítása után egy promptot jelenít meg, melyen várja a felhasználótól, hogy
adjon meg szintaktikailag és szemantikailag helyes logikai kifejezéseket, mellyel a továbbiakban dolgozni tud. A program lehetőséget biztosít a maga szerény módján "változók bevezetésére" is. Ezeket egy
értékadás művelettel tudjuk deklarálni és definiálni is egyben.

A logikai kifejezések a következő építőkockákból állnak:

  - A legalapvetőbb, két db logikai literál, azaz az 1 (igaz) és a 0 (hamis). A program jelenleg ezt a két karaktert tekinti csak valid literálnak. Ez azért van, mert bár lehetett volna még a különböző string reprezentációkat is figyelni egy összetettebb regexp kifejezéssel, de akkor túlságosan bonyolulttá vált volna a tokenkezelés. Jelenleg a feldolgozás során minden 0 = hamis, minden 1 és annál nagyobb számjegy = igaznak értékelődik ki; ez igazából nem jelent a működésre nézve további fennakadásokat, de a konvertálási technikából származó tulajdonságként mindenképpen megemlítendő.
  
- Az implementált logikai operátorok: AND (and, &&), OR (or, ||), XOR (xor, ^), NOT (not, !)
Mint látható, itt már a program képes felismerni a csak nagybetűsített, csak kisbetűs, illetve a karakterükkel megadott operátorokat is.

- Változók bevezetése, melyeket a következő egyszerű módon tudunk deklarálni és definiálni:
v_a = 1 vagy vb = 0, illetve v_logikai_literal = 1.
Minden változó neve kötelezően kis v betűvel kell hogy kezdődjön, majd ezt követve minimum egy (de tetszőleges számú) kisbetű, nagybetű, szám, illetve alahúzasjel konkatenációja által alkotott string.
Ha helytelen változót próbálunk bevezetni, arról hibaüzenetet fogunk kapni.

Most hogy az alapvető építőkockákat ismerjük, nézzünk példákat sorban a fentiek használatára:
- Nézzük meg a következő kifejezéseket, milyen eredményt kapunk:

BoolCalc>>> 1 AND 1

('AND', True, True)

True

Az egyes sorok részletes jelentése:
Az első sorban láthatjuk a beviteli sort, ahová beírhatjuk a parancsot.
A második sorban azt láthatjuk, milyen szintaxis-fa felépülését eredményezi a bevitt kifejezés.
Jelen esetben azt láthatjuk, hogy két igaz literál között teremtettünk egy ÉS kapcsolatot.
A harmadik sor szolgáltatja az egész kifejezés kiértékelése után előálló végeredményt.
Jelen esetben ez egy igaz érték.

Ha csak egy literált vizsgálunk, mint kifejezést, természetesen annak a szintaxis-fája önmaga, és "ki tudjuk értékelni" csak azt is:

BoolCalc>>> 1

True

True


BoolCalc>>> 0

False

False

Természetesen a szintaxis-fa miatt lehetővé válik, hogy tetszőlegesen összetett kifejezéseket kombináljunk egymással, és ezeket vizsgáljuk:

BoolCalc>>> 1 AND 0 OR 1 AND NOT 0
('OR', ('AND', True, False), ('AND', True, True))
True

A fenti kifejezés értéke mint láthatjuk igaz. Itt azonban elő is jön a logikai operátorok közötti
precedencia kérdése, melyet a program képes az általunk beállítottak szerint lekezelni.
Jelen esetben, az ÉS operátorok által elvégzett műveletek kiértékelése után következik a VAGY operátor
végrehajtása. Ez a viselkedés helyes, hiszen mint azt a kódban láthatjuk is, a logikai operátorok precedenciáját a következő sorrendben határoztuk meg:
NOT > AND > OR, XOR.

Nézzünk példát egy mégbonyolultabb kifejezésre, ahol már fölváltva használjuk a különböző logikai operátorok reprezentációit is!

BoolCalc>>> NOT NOT NOT 1

False

False

BoolCalc>>> 1 or 0 XOR not 0 AND 0

('XOR', ('or', True, False), ('AND', True, False))
True

BoolCalc>>> 0 XOR 1 or 1 and NOT not 0 && 1 or !1 ^ 0 || 1


('||', ('^', ('or', ('or', ('XOR', False, True), ('&&', ('and', True, False), True)), False), False), True)

True

Mint láthatjuk, ez sem okoz problémát a kiértékelésben. A következőben próbáljunk meg szintaktikailag hibás kifejezést megadni:

BoolCalc>>> 1 OR 1 AND AND 1

Szintaxis hiba a bemeneten!

True

True

A fentiek esetén a két egymást követp ÉS operandust természetesen szintaktikai hiábnak érzékelte a program. Ilyen esetben is mint látjuk, a "maradék" tokenekből előállít egy eredményt, viszont ez az eredmény mivel szemantikailag eléggé aggályos kifejezésből származik, ezért helyességére nem éri meg alapozni :)

Példák helyes változó bevezetésére, majd annak értékének lekérdezésére:

BoolCalc>>> v_a = 1

('=', 'v_a', True)

A már inicizalizált változók értéke bármikor felülírható az értékadó kifejezés ismétlésével a már létező változónévem. Illetve az adott változó tartalmát bármikor le is kérdezhetjük:

BoolCalc>>> v_a

('valtozo', 'v_a')

True






