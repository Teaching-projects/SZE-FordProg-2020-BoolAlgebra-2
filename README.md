# SZE-FordProg-2020-BoolAlgebra-2
Hollosy Adam

Boolean Kalkulátor

Ebben a kis python programban egy végtelenül egyszerű boolean kifejezéseket kiértékelő kalkulátor
megvalósítását tűztem ki célul. Nyilván a projekt elsődleges célja, hogy a Ply lex és yacc python
implementációjának használatában mélyedjek kicsit el, így a képességei igencsak limitáltak,
viszont a Ply elemeivel való ismerkedés jól mutatja, milyen hatékony eszköz lehet egy nagyobb
projektben használva, amennyiben tokenizálásra és parseolásra lenne szükség.

A funkciók bemutatása:

A kalkulátor az elindítása után egy promptot jelenít meg, melyen várja a felhasználótól, hogy
adjon meg szintaktikailag és szemantikailag helyes logikai kifejezéseket, mellyel a továbbiakban dolgozni tud.

A logikai kifejezések a következő építőkockákból állnak:

  - A legalapvetőbb, két db logikai literál, azaz az 1 (igaz) és a 0 (hamis). A program jelenleg ezt a két karaktert tekinti csak valid literálnak. Ez azért van, mert bár lehetett volna még a különböző string reprezentációkat is figyelni egy összetettebb regexp kifejezéssel, de akkor túlságosan bonyoluláttá vált volna a tokenkezelés. Jelenleg a feldolgozás során minden 0 hamis, minden 1 és annál nagyobb számjegy igaznak értékelődik ki, de ez igazából nem jelent a működésre nézve további fennakadásokat.
  
- Az implementált logikai operátorok: AND (and, &&) OR (or, ||) XOR (xor, ^) NOT (not, !)
Mint látható, itt már a program képes felismerni a csak nagybetűsített, csak kisbetűs, illetve a karakterekkel megadott operátorokat is.

Példa:
Tehát az előzőek alapján a következő kifejezéseket kombinálhatjuk össze

