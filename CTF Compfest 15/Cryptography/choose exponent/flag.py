from z3 import *

c1 = 10585687135261482772876922503990004971257920012770151734429900590445750171877343407101707695153308673075948460341230728626997517474052124808944767708576096317317149524749914734832463138759437006813513223545874257434758567562943830788988447346439253837531387065150714801969466351140450501721621636115613331408174114252286339522296211385630995308147648507773461044495711264569854511657726606900729201147373172428887890274835314531321309628430695451881378849095169754903909183881790617941767262878561561082401873583521866358819057545079680270185769875287251217162943235043571377752126277756872962194659934507151453653925
c2 = 3591966630904052565511695790164807604542516325264868938629400988058026429471788611055709730703328972104187734950268209261769834218270580397511446268327949765316459129173636858775871499402902296108421519805493356430934557180679408939286641422208190926957744635675881739545101473739606245518851809113439757745904856774022610513983795864695316710153715960588405014275147813129186032428054729527296000583917288880395209069404261115854097742142977588470500169945830885810560999018662197341851087017039393937554764589655750890442280789172885266202799496405601073783954274116405901621709479385460850110942389747228932989779
c3 = 4643075872228582580531793969086900745863722806205630002804159950222294607714521413621141075486838091017712463239182277983595971417689948168044613688075967603922356440195936604266400891815263534393507685874734508323630317194265699819927418458140250429539657163432303465924761323450602666701626113650207486179754007027867454051568652103793367284007145477664911412081168031538701374452155319297194222411611207259446198063227142277587814556824067017824154921986168733831961548652618887076295127305985459719326513194507246563351137717585795137954601262054840395137327836604462896744631329459353858194189053759866663701205

e1 = 3
e2 = 5
e3 = 7

s = Solver()
m, N = Ints("m N")
s.add(pow(m, e1) % N == c1)
s.add(pow(m, e2) % N == c2)
s.add(pow(m, e3) % N == c3)

print(s.sat())