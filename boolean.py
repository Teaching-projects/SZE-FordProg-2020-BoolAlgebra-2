import ply.lex as lex
import ply.yacc as yacc
import sys


# Az osszes hasznalatban levo tokenunket tartalmazo lista definialasa

tokens = [

 'BOOLEAN',
 'AND',
 'OR',
 'XOR',
 'NOT',
 'EQUALS',
 'VARIABLE'

]


# Regularis kifejezesek segitsegevel leirjuk az (egyszerubb) tokenek felepiteset,
# mely alapjan a lexer azonosithatja majd oket

t_AND = r'AND|and|&&'
t_OR = r'OR|or|\|\|'
t_XOR = r'XOR|xor|\^'
t_NOT = r'NOT|not|!'
t_EQUALS = r'\='


# A Ply beepitett t_ignore specialis tokennel felsorolhatjuk, mely karaktereket
# hagyja figyelmen kivul a lexer. Esetunkben ez most csak a space

t_ignore = r' '


# Az osszetettebb tokeneket fuggvenyek segitsegevel definialhatjuk
# a Ply szamara. Ezek a fuggvenyek kovetkeznek

# A boolean literal tokenert felelos fuggveny kicsit trukkos.
# Lehetett volna stringkent is figyelni a lehetseges ertekeit, azoknak
# kulonbozo szoveges reprezentacioit, de az egyszeruseg kedveert
# csak az elterjedt 1 (igaz/true) es a 0 (hamis/false) karaktereket figyeljuk.
# A stringet (ami valid ertek eseten most csak szigoruan egy karakter hosszu lehet)
# eloszor int-te alakitjuk, majd onnan boolean-na, emiatt a 0,1 vart
# ertekeken kivul minden mas (2-9) szam szinten igaz ertekke alakul.
# Amennyiben tobb szamjegy is koveti egymast, szintaxis-hibat jelzunk

def t_BOOLEAN(t):
 r'\d'
 t.value = bool(int(t.value))
 return t


# A VARIABLE a valtozokert felelos token.
# Egy valtozo neve lehetne akar tetszoleges betuvel kezdodo alfanumerikus
# string is, de egyszerubbnek iteltem meg, ha annyi megkotest hozzaadok
# a valtozonev konvenciohoz, hogy kotelezo kis v-vel kezdodnie;
# igy kikuszoboltem, hogy a logikai muveletek megadasara szolgalo fenntartott
# szavakkal "osszeakadjon" a dolog. Termeszetesen joval bonyolultabb regularis
# kifejezes hasznalataval a megkotest ki lehetett volna valtani, de igy sokkal
# egyszerubb volt a lehetseges problemak elkerulese.
# A valtozonev konvencio tehat:
# v, majd ezt kovetve minimum egy (de tetszoleges szamu)
# kisbetu, nagybetu, szam, illetve alahuzasjel konkatenacioja altal alkotott string

def t_VARIABLE(t):
 r'v[a-zA-Z_0-9]+'
 t.type = 'VARIABLE'
 return t


# Amennyiben nem a fentieknek megfeleltetheto es felismert tokent talalunk,
# akkor a karaktereket egyszeruen skippeljuk a lexer altal.
# Erre a Ply specialis t_error fuggvenyenek hasznalataval van lehetoseg

def t_error(t):
 print("Nem megengedett karakter erkezett a bemeneten!")
 t.lexer.skip(1)


# A lexer letrehozasa

lexer = lex.lex()

# Az altalunk definialt muveleti sorrendet szeretnenk biztositani a kifejezesek
# feldolgozasa soran. Logikai muveleti precedencia a legtobb (C szeru) nyelv eseten
# altalaban a kovetkezo: NOT, AND, OR (XOR).
# Ezt a Ply specialis precedence valtozojanak megadasaval allithatjuk be

precedence = (

 ('left', 'OR', 'XOR'),
 ('left', 'AND'),
 ('left', 'NOT'),

)


# Kovetkezik a nyelvtanunk megadasa.
# Az alabbiakat engedelyezzuk a nyelvtanunkban: expression, assign_variable es empty 
# Kezdoszabalynak a boolean_calculator nem-terminalist adjuk meg

def p_boolean_calculator(p):
 '''
 boolean_calculator : expression
                    | assign_variable
                    | empty
 '''

# Irjuk ki a kifejezest reprezentalo szintaxis-fat

 print(p[1])

# Jarjuk is be a fat, es hajtsuk vegre kozben az eloirt logikai muveleteket,
# majd irjuk ki a kifejezes eredmenyet

 print(run(p[1]))


# A nyelvtanunkban szereplo kifejezesek becserelesehez rendelkezesre allo szabalyok

def p_expression(p):
 '''
 expression : expression AND expression
            | expression OR expression
            | expression XOR expression               
 '''

 # A szintaxis-fa epitese

 p[0] = (p[2], p[1], p[3])


# A nyelvtanunkban szereplo valtozo megadasara es ertekadasara szolgalo szabaly

def p_assign_variable(p):
 '''
 assign_variable : VARIABLE EQUALS expression
 '''
 p[0] = ('=', p[1], p[3])


# A nyelvtanunkban szereplo kifejezes negaciojara szolgalo szabaly

def p_expression_not(p):
 '''
 expression : NOT expression       
 '''
 p[0] = not p[2]


# A nyelvtanunkban szereplo boolean literal terminalis szabalya

def p_expression_boolean(p):
 '''
 expression : BOOLEAN           
 '''
 p[0] = p[1]


# A nyelvtanunkban szereplo valtozo terminalis szabalya

def p_expression_variable(p):
 '''
 expression : VARIABLE
 '''
 p[0] = ('valtozo', p[1])


# Amennyiben a bemenetrol a lexer olyan token-sorozatot allitott elo,
# ami nem teljesiti az elore definialt nyelvtanunkat,
# ezt a parsernek jeleznie kell a felhasznalonak.
# Erre a Ply biztosit egy specialis fuggvenyt, a p_error-t

def p_error(p):
 print("Szintaxis hiba a bemeneten!")


# Mivel a nyelvtanunkban hasznaltuk az empty kifejezest, ezert utolso lepeskent
# az ezt leiro szabalyt is meg kell adnunk

def p_empty(p):
 '''
 empty :
 '''
 p[0] = None


# A parser letrehozasa

parser = yacc.yacc()


# Hozzunk letre egy szotarat, melyben tarolni fogjuk a valtozokat;
# kulcs-ertek parokban. Amikor definialunk egy valtozot, az ide kerul be,
# illetve, amikor hasznaljuk egy kifejezesben, akkor innen kerul kiolvasasra

dictionary = {}


# A run fuggveny fogja bejarni a fentiek altal generalt szintaxis-fat es hatja
# vegre kozben a szukseges logikai muveleteket.
# Mint az lathato, ez egy rekurziv fuggveny

def run(p):
 global dictionary	
 if type(p) == tuple:
  if p[0] == 'AND' or p[0] == 'and' or p[0] == '&&':
   return run(p[1]) and run(p[2])
  elif p[0] == 'OR' or p[0] == 'or' or p[0] == '||':
   return run(p[1]) or run(p[2])
  elif p[0] == 'XOR' or p[0] == 'xor' or p[0] == '^':
   return run(p[1]) != run(p[2])
  elif p[0] == 'NOT' or p[0] == 'not' or p[0] == '!':
   return not run(p[2])
  elif p[0] == '=':
   dictionary[p[1]] = run(p[2])
   return ''
  elif p[0] == 'valtozo':
   if p[1] not in dictionary:
    return 'Nem definialt valtozo!'
   else:
    return dictionary[p[1]]
 else:
  return p


# Nincs mas hatra, mint beallitani, hogy a bemeneti string jelen esetben
# a szabvanyos bemenetrol, azaz most a billentyuzetrol erkezzen

while True:
 try:
  s = input('BoolCalc>>> ')
 except EOFError:
  break
 parser.parse(s)
