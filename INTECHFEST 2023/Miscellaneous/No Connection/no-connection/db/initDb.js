db = new Mongo().getDB("flagdb");

db.createCollection('flag');

db.flag.insert([
    { "flag": "fake flag 1" },
    { "flag": "fake flag 2" },
    { "flag": process.env['FLAG'] },
    { "flag": "fake flag 3" }
])
