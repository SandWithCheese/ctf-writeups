function boo() {
  // You found part one:)
  alert("BOO! ahh! You found part one... -> NICC{gh0sts")
}

function graveyardSmash() {
  const skeles = document.getElementsByClassName("skellys")
  for (const skelly of skeles) {
    skelly.src = "skelly.png"
  }
}

function huntGhostsAndMonsters(
  ectoplasm,
  specter,
  poltergeist,
  goblin,
  apparition
) {
  let paranormalEntityCount = 0
  let ghostlyManifestation = false

  for (let i = 0; i < ectoplasm.length; i++) {
    if (ectoplasm[i] === specter) {
      paranormalEntityCount++
    }
  }

  if (paranormalEntityCount > 0) {
    ghostlyManifestation = true
  }

  while (ghostlyManifestation) {
    for (let j = 0; j < poltergeist.length; j++) {
      if (poltergeist[j] === goblin) {
        paranormalEntityCount--
      }
    }

    if (paranormalEntityCount === 0) {
      break
    }
  }

  let exorcismSuccessful = false

  if (apparition) {
    exorcismSuccessful = true
  }

  if (exorcismSuccessful) {
    return "Ghosts and monsters have been banished!"
  } else {
    return "The supernatural persists..."
  }
}

const ectoplasmicEvidence = [1, 2, 3, 4, 5]
const ghostlySpecter = 3
const hauntedPoltergeist = [5, 6, 7]
const mischievousGoblin = 6
const apparitionExists = true
console.log(
  huntGhostsAndMonsters(
    ectoplasmicEvidence,
    ghostlySpecter,
    hauntedPoltergeist,
    mischievousGoblin,
    apparitionExists
  )
)

function summonCursedSpirits(banshee, wraith, zombie, poltergeist, phantom) {
  let paranormalActivity = false
  let ghostlyEncounter = 0

  for (let i = 0; i < banshee.length; i++) {
    if (banshee[i] === wraith) {
      ghostlyEncounter++
    }
  }

  if (ghostlyEncounter > 0) {
    paranormalActivity = true
  }

  while (paranormalActivity) {
    for (let j = 0; j < zombie.length; j++) {
      if (zombie[j] === poltergeist) {
        ghostlyEncounter--
      }
    }

    if (ghostlyEncounter === 0) {
      break
    }
  }

  let ritualSuccessful = false

  if (phantom) {
    ritualSuccessful = true
  }

  if (ritualSuccessful) {
    return "Cursed spirits have been summoned and dismissed!"
  } else {
    return "The incantation failed to manifest anything..."
  }
}

// Example usage:
const bansheeCall = [1, 2, 3, 4, 5]
const wailingWraith = 3
const zombieLegion = [5, 6, 7]
const mischievousPoltergeist = 6
const spectralPhantom = true

console.log(
  summonCursedSpirits(
    bansheeCall,
    wailingWraith,
    zombieLegion,
    mischievousPoltergeist,
    spectralPhantom
  )
)

function printSpookyArray() {
  const spookyItems = [
    "The website flickered_with_ghostly code.",
    "Eerie whispers echoed in the digital void.",
    "Spectral images materialized_on the screen.",
    "Phantom clicks and keystrokes haunted the interface.",
    "Cursed data corrupted the webpage.",
    "The cursor moved as if_guided by unseen hands.",
    "A chilling presence_lingered in the browser.",
    "Cryptic symbols appeared in the source code.",
    "Links led to mysterious_and forbidden pages.",
    "The website's soul seemed lost in the code.",
    "Images_warped_into disturbing forms.",
    "Browsers froze in fear of the haunted site.",
    "Ghostly animations danced across the screen.",
    "Passwords changed on their_own accord.",
    "The website's flags_shifted to NICC{, but this was not one of them.",
    "Users reported strange and eerie pop-ups.",
    "The server logs_were_filled with cryptic messages.",
    "The website's pages seemed to rewrite themselves.",
    "Haunted links led to unknown realms.",
    "The site's domain was cursed by a malevolent spirit.",
    "E-mails from the beyond flooded the inbox.",
    "The search bar summoned eldritch results.",
    "The blog posts were haunted by ghostwriters.",
    "A ghost in the machine wreaked havoc on the layout.",
    "The navigation menu led to a ghost town.",
    "In the dark corners of the code, spirits whispered.",
    "The site's database contained lost souls of data.",
    "A cursed API returned spectral data.",
    "The login screen was guarded by a spectral guardian.",
    "Ectoplasmic glitches infected the JavaScript.",
    "Cursed forms submitted data to the netherworld.",
    "The site's SSL certificate was haunted by expired ghosts.",
    "404 pages displayed the faces of restless spirits.",
    "The homepage was an eerie portal to the unknown.",
    "Ghostly pixels haunted the image gallery.",
    "They shouted that you found the third!: cky_2_s33_b",
    "The site's footer contained cryptic incantations.",
    "The blog comments were filled with ghostly praise.",
    "Users reported being followed by digital apparitions.",
    "The website's sitemap led to a spectral maze.",
    "The site's analytics were haunted by phantom visitors.",
    "The FAQ section answered questions from beyond.",
    "E-mails sent from the site vanished into the abyss.",
    "Cursed cookies possessed the user's browser.",
    "The terms and conditions were written in ghostly ink.",
    "The site's contact form summoned spectral inquiries.",
    "The homepage's hero image was a cursed portrait.",
    "Pop-up notifications delivered cryptic prophecies.",
    "The loading spinner was possessed by impatience.",
    "A ghostly chatbot offered spectral customer support.",
    "The site's error messages spoke in riddles.",
    "The CAPTCHA was a test of one's psychic abilities.",
    "The site's forums were haunted by restless souls.",
    "User accounts were plagued by poltergeist passwords.",
    "The website's source code contained a haunted comment.",
    "The footer contained a link to the spirit world.",
    "The login screen asked for a secret from the afterlife.",
    "The privacy policy warned of spectral data collection.",
    "Ghostly images appeared in the image carousel.",
    "Cursed CSS styles warped the site's appearance.",
    "The site's AI chatbot conversed with ghostly wisdom.",
    "Ghostly SEO techniques boosted the site's ranking.",
    "The newsletter sign-up summoned spectral subscribers.",
    "The site's cookies were possessed by hungry spirits.",
    "A cursed pop-up window asked for your soul.",
    "The website's dark theme was haunted by shadows.",
  ]

  for (let i = 0; i < spookyItems.length; i++) {
    console.log(spookyItems[i])
  }
}

// Call the function to print the spooky items
printSpookyArray()
