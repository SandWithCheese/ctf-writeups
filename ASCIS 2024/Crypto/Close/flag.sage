from math import gcd

N_prime = [
    2130976337586005237156464206440420238795565461269490301585855909243137947798414127770622674742724352434331955896863644115665473805181972333821798148318799414303412313764438520452979811024935800578317205194535118744206321140383615692221976332951446168327815156707303807757477643618478178097808590013870602530571978483874107959618249495480404703039921462919059600508942634416478729156246889530274312285677320148095767520776395382610426929918977563944737154815051073804770658613252320954771991606103098402264525379694922957368418168481371020472830737481531266630093221880319725471683836854133653864083162346785113297683705360085961158753163727611496209455438221912781269299711779832658189935673806833012531569328477760118728288998405856941007991900725659274293982786073642879717420962731703476868833118161112664313792413800564596946051574011354351831603624300154840811613782989056951172522500835314687914163366650332659633288163,
    2724037318674271086650447702070622375034861255304438717212172859171502986139415815041303457248662898812636029870181169539698582157596678976319885943602013615596314541242314223796153426926255235152668722870474200290619913816825637578268245306697316483895912232417073776730330891849576569682680319366880421269826884414700000757784798502289304103210140185862955753436603722506089178809949852990108336262759717632367946203946246293777315895381895311165687091955990889229787046729823535584170695122315779869883592318911535794642950406414658398131464828814786912910452684500515681764429615217619353314875027749599080323389716386057532469740854693102887806019415096201152871365561547406714917294252954637321114547657092913684836104437438009065254935303766017775862067651265645828848328151185935792297944544632491664122092606459921464368198588017057047648122587163017214781076851088421955611649541557810984363440551831480883100894756,
    3383691878575471137089480888231172217866372258737361724957049521443443763029492809957409855991601293006223529553883773627262495918396580897315269393280090785607968778675228571143800897710500032700970973479956266461645024228597797295405062451269007563713263628196000287257749403776819070878113025521171955244378522212336359386213357451545050706081701069044868262458018932816656573810080433013346290226230600368695800792576148525630013674812581362450498826742727103970523587676787319516950204652226049894689926060531804700811668476231071908657043230214206125790484400070750115887590529367278059485685813618860125616508009373173700272979627354838587983949365228826137095388053111649098562302326183354472597204968565593722161991837351387615485549721520279021350590308413210999753314846116160847470647157455724360861290543130383536365633765271408624374535169271534024038682821784256903999466933064864745320489800372659636332745046,
    3332851029830030020505312984858653864345835268092239580990493634816507465430956556762570304817073168605608529751959654545598713625624868535189519475633800845574486091187281279194464271600451330990793201223344729337160440769167384107356313334614380612681788939375289389552144092580754111812673799210293171571982790813487441850940616422874478885343212354265965733309928658793814208027091847421067475414218368539114727554252047972983373810874608325994896019236467640264187075166139858244443447044173305977034944223075961886821726913126402563633247855133971551147199604314569161069733929079286010685677153823781994220227408147047766849481286415120189298226090927049839969843135486078365496550479979529714310517104538163512763611247082326619524794973225502128429325265447729855527054260487797674749859721550631596291203249557847087262131821860919842254911909880721230913107733946362614921747812086494067811669012763198977877196090,
]

# The approximate size of the original N (since N' and N differ by small noise)
approx_N = 2 ^ 3072

# A lattice matrix to capture the relation N'_i = N_i + delta_i
# We create a 5x5 matrix for 4 moduli and a noise term
matrix_entries = [
    [approx_N, 0, 0, 0, N_prime[0]],
    [0, approx_N, 0, 0, N_prime[1]],
    [0, 0, approx_N, 0, N_prime[2]],
    [0, 0, 0, approx_N, N_prime[3]],
    [0, 0, 0, 0, 2 ^ 256],  # Noise constraint
]

# Construct the lattice matrix in Sage
L = Matrix(ZZ, matrix_entries)

# Perform LLL reduction on the lattice matrix
L_reduced = L.LLL()

# Print the reduced matrix
print("LLL Reduced Matrix:")
print(L_reduced)

# Recover original N values by subtracting small vectors (assumed to be noise)
recovered_N = []
for i in range(4):
    delta_i = L_reduced[i, 4]  # Noise term from the reduced matrix
    # print(delta_i)
    N_i = N_prime[i] - delta_i  # Recover the original N_i
    recovered_N.append(N_i)

for i in range(4):
    for j in range(i + 1, 4):
        gcd_val = gcd(recovered_N[i], recovered_N[j])
        if gcd_val != 1:
            print(f"Common factor found: {gcd_val}")
            print(f"i: {i}, j: {j}")