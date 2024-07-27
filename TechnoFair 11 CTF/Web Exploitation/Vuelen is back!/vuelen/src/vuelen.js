const Vue = require('vue');
const renderer = require('vue-server-renderer').createRenderer();
const axios = require('axios');

async function fetchCoins() {
    try {
        const response = await axios.get('https://api.reku.id/v2/coins');
        return response.data.result;
    } catch (error) {
        console.error('Error fetching coins:', error);
        return [];
    }
}

function GenerateHTML(input, data) {
    let filteredData = data;
    if (input) {
        filteredData = data.filter(coin => coin.accountcode.toLowerCase().includes(input.toLowerCase()));
    }

    let coinlist = '<ul>';
    filteredData.forEach(coin => {
        coinlist += `<div class="coin"><span>${coin.accountname}</span></div>`;
    });
    coinlist += '</ul>';


    var pre_template = `
      <!DOCTYPE html>
      <html>
      <head>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>Vuelen</title>
          <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
      </head>

      <body>
          <style type="text/css">
              body {
                  background:
                      radial-gradient(farthest-side at -33.33% 50%, #0000 52%, #474bff 54% 57%, #0000 59%) 0 calc(128px/2),
                      radial-gradient(farthest-side at 50% 133.33%, #0000 52%, #474bff 54% 57%, #0000 59%) calc(128px/2) 0,
                      radial-gradient(farthest-side at 133.33% 50%, #0000 52%, #474bff 54% 57%, #0000 59%),
                      radial-gradient(farthest-side at 50% -33.33%, #0000 52%, #474bff 54% 57%, #0000 59%),
                      #130f40;
                  background-size: calc(128px/4.667) 128px, 128px calc(128px/4.667);

              }

              .glitch-wrapper {
                  width: 100%;
                  height: 100%;
                  display: flex;
                  align-items: center;
                  justify-content: center;
                  text-align: left;
              }

              .glitch {
                  position: relative;
                  font-size: 40px;
                  font-weight: 700;
                  line-height: 1;
                  color: #fff;
                  letter-spacing: 5px;
                  z-index: 1;
              }

              .glitch:before {
                  content: attr(data-glitch);
                  position: absolute;
                  top: 0;
                  left: -2px;
                  width: 100%;
                  color: #fff;
                  overflow: hidden;
                  clip: rect(0, 900px, 0, 0);
                  animation: noise-before 3s infinite linear alternate-reverse;
              }

              .glitch:after {
                  content: attr(data-glitch);
                  position: absolute;
                  top: 0;
                  left: 2px;
                  width: 100%;
                  color: #fff;
                  overflow: hidden;
                  clip: rect(0, 900px, 0, 0);
                  animation: noise-after 2s infinite linear alternate-reverse;
              }

              @keyframes noise-before {
                  0% {
                      clip: rect(61px, 9999px, 52px, 0);
                  }

                  5% {
                      clip: rect(33px, 9999px, 144px, 0);
                  }

                  10% {
                      clip: rect(121px, 9999px, 115px, 0);
                  }

                  15% {
                      clip: rect(144px, 9999px, 162px, 0);
                  }

                  20% {
                      clip: rect(62px, 9999px, 180px, 0);
                  }

                  25% {
                      clip: rect(34px, 9999px, 42px, 0);
                  }

                  30% {
                      clip: rect(147px, 9999px, 179px, 0);
                  }

                  35% {
                      clip: rect(99px, 9999px, 63px, 0);
                  }

                  40% {
                      clip: rect(188px, 9999px, 122px, 0);
                  }

                  45% {
                      clip: rect(154px, 9999px, 14px, 0);
                  }

                  50% {
                      clip: rect(63px, 9999px, 37px, 0);
                  }

                  55% {
                      clip: rect(161px, 9999px, 147px, 0);
                  }

                  60% {
                      clip: rect(109px, 9999px, 175px, 0);
                  }

                  65% {
                      clip: rect(157px, 9999px, 88px, 0);
                  }

                  70% {
                      clip: rect(173px, 9999px, 131px, 0);
                  }

                  75% {
                      clip: rect(62px, 9999px, 70px, 0);
                  }

                  80% {
                      clip: rect(24px, 9999px, 153px, 0);
                  }

                  85% {
                      clip: rect(138px, 9999px, 40px, 0);
                  }

                  90% {
                      clip: rect(79px, 9999px, 136px, 0);
                  }

                  95% {
                      clip: rect(25px, 9999px, 34px, 0);
                  }

                  100% {
                      clip: rect(173px, 9999px, 166px, 0);
                  }
              }

              @keyframes noise-after {
                  0% {
                      clip: rect(26px, 9999px, 33px, 0);
                  }

                  5% {
                      clip: rect(140px, 9999px, 198px, 0);
                  }

                  10% {
                      clip: rect(184px, 9999px, 89px, 0);
                  }

                  15% {
                      clip: rect(121px, 9999px, 6px, 0);
                  }

                  20% {
                      clip: rect(181px, 9999px, 99px, 0);
                  }

                  25% {
                      clip: rect(154px, 9999px, 133px, 0);
                  }

                  30% {
                      clip: rect(134px, 9999px, 169px, 0);
                  }

                  35% {
                      clip: rect(26px, 9999px, 187px, 0);
                  }

                  40% {
                      clip: rect(147px, 9999px, 137px, 0);
                  }

                  45% {
                      clip: rect(31px, 9999px, 52px, 0);
                  }

                  50% {
                      clip: rect(191px, 9999px, 109px, 0);
                  }

                  55% {
                      clip: rect(74px, 9999px, 54px, 0);
                  }

                  60% {
                      clip: rect(145px, 9999px, 75px, 0);
                  }

                  65% {
                      clip: rect(153px, 9999px, 198px, 0);
                  }

                  70% {
                      clip: rect(99px, 9999px, 136px, 0);
                  }

                  75% {
                      clip: rect(118px, 9999px, 192px, 0);
                  }

                  80% {
                      clip: rect(1px, 9999px, 83px, 0);
                  }

                  85% {
                      clip: rect(145px, 9999px, 98px, 0);
                  }

                  90% {
                      clip: rect(121px, 9999px, 154px, 0);
                  }

                  95% {
                      clip: rect(156px, 9999px, 44px, 0);
                  }

                  100% {
                      clip: rect(67px, 9999px, 122px, 0);
                  }
              }

              .coin {
                  width: auto;
                  padding-left: 15px;
                  padding-right: 15px;
                  height: 80px;
                  display: inline-block;
                  background-color: #fff;
                  border-radius: 5px;
                  background: rgba(104, 109, 224, 0.5);
                  -webkit-backdrop-filter: blur(10px);
                  backdrop-filter: blur(10px);
                  border: 1px solid rgba(104, 109, 224, 0.25);
                  color: #fff;
                  text-align: center;
                  padding-top: 25px;
                  margin: 3px 3px;
              }
          </style>
          <div class="container">
              <div class="row justify-content-center align-item-center">
                  <div class="col-sm-4 text-center pt-5 pb-5">
                      <img src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/d786ae4e-d391-4919-9c7b-1ef9af045540/dgc608c-a0dbc9c3-bf5b-478e-b8c8-8c4acdcbae13.png/v1/fill/w_1280,h_720/nolan_voidwalker_basic_skin_mlbb_png_by_yenagry_dgc608c-fullview.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NzIwIiwicGF0aCI6IlwvZlwvZDc4NmFlNGUtZDM5MS00OTE5LTljN2ItMWVmOWFmMDQ1NTQwXC9kZ2M2MDhjLWEwZGJjOWMzLWJmNWItNDc4ZS1iOGM4LThjNGFjZGNiYWUxMy5wbmciLCJ3aWR0aCI6Ijw9MTI4MCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.D7WGzWg3DPJdmqm5Sw_e1wkxFUDLcGT3bgorHN5wgr0"
                          alt="Nolan MLBB" style="width: 76%;" class="mx-auto" />
                  </div>

                  <div class="col-sm-4">
                      <div class="glitch-wrapper">
                          <div class="glitch" data-glitch="McLaren Vue Warna Apa Bos?">McLaren Vue Warna Apa Bos?</div>
                      </div>
                  </div>

                  <div class="col-sm-7">
                      <form action="/" method="post">
                          <input type="text" name="name" value="${input}" placeholder="Filter" class="form-control"
                              style="width: 84%;display: inline-block;">
                          <input type="submit" value="Find" class="btn btn-primary" style="width: 15%;">
                      </form>
                  </div>

                  <h4 class="text-white">Search : ${input}</h4>
                  <div class="col-sm-10">
                      <div class="mt-5 mb-5 text-center">
                          ${coinlist}
                      </div>
                  </div>
              </div>
          </div>
          <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script></body></html>
      `;

    var app = new Vue({ template: pre_template });

    return new Promise((resolve, reject) => {
        renderer.renderToString(app, (err, result) => {
            if (err) reject(err);
            resolve(result);
        });
    });
}

module.exports = function (app, baseURI) {
    app.post(baseURI + '/', async (request, response) => {
        try {
            var blacklist = ['global', 'require', 'child_process', 'exec'];
            var input = request.body.name || "";

            if (blacklist.includes(input)) {
                input = "blacklist";
            }

            var requester = await fetchCoins();
            var html = await GenerateHTML(input, requester);
            response.send(html);
        } catch (err) {
            console.log(err);
        }
    });

    app.get(baseURI + '/', async (request, response) => {
        try {
            var requester = await fetchCoins();
            var html = await GenerateHTML("", requester);
            response.send(html);
        } catch (err) {
            console.log(err);
        }
    });
};
