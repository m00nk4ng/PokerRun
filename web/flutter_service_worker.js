'use strict';
const MANIFEST = 'flutter-app-manifest';
const TEMP = 'flutter-temp-cache';
const CACHE_NAME = 'flutter-app-cache';

const RESOURCES = {"flutter_bootstrap.js": "d4a81c5ddf84cf91cf4229eff0d1063f",
"version.json": "f0c7b80ce961deb4cbe117329c69308d",
"index.html": "be1548a04dc71c6adc678eefb60dc4bd",
"/": "be1548a04dc71c6adc678eefb60dc4bd",
"main.dart.js": "3de9859eac86272907ba6970577d95b1",
"config.json": "b56b749245657da89aeda6b7f3e1c6ce",
"flutter.js": "888483df48293866f9f41d3d9274a779",
"favicon.png": "5dcef449791fa27946b3d35ad8803796",
"icons/Icon-192.png": "ac9a721a12bbc803b44f645561ecb1e1",
"icons/Icon-maskable-192.png": "c457ef57daa1d16f64b27b786ec2ea3c",
"icons/Icon-maskable-512.png": "301a7604d45b3e739efc881eb04896ea",
"icons/Icon-512.png": "96e752610906ba2a93c65f8abe1645f1",
"manifest.json": "ba20ae3473a61ce74d28afe91ff762dd",
"assets/AssetManifest.json": "9e10b2b4e2dc2cc926ea1b29bd39764e",
"assets/NOTICES": "941c65e7cf7a6df1c0e22d6e480236b4",
"assets/FontManifest.json": "279bcf93fb1616d6d2939001d0b72a9e",
"assets/AssetManifest.bin.json": "bbe6d9c3d94cafa833bc1dae7c70a378",
"assets/packages/cupertino_icons/assets/CupertinoIcons.ttf": "33b7d9392238c04c131b6ce224e13711",
"assets/packages/font_awesome_flutter/lib/fonts/Font-Awesome-7-Free-Regular-400.otf": "2b47c4b9f90c6327cbce0436794cfe84",
"assets/packages/font_awesome_flutter/lib/fonts/Font-Awesome-7-Brands-Regular-400.otf": "1fcba7a59e49001aa1b4409a25d425b0",
"assets/packages/font_awesome_flutter/lib/fonts/Font-Awesome-7-Free-Solid-900.otf": "f8180c98905702c637985c8714d0954b",
"assets/shaders/ink_sparkle.frag": "ecc85a2e95f5e9f53123dcaf8cb9b6ce",
"assets/AssetManifest.bin": "91dd335d87ef8009c9cb2890eaef5091",
"assets/fonts/MaterialIcons-Regular.otf": "e79089dd3c7722ddbbdcd5e3c0846b06",
"assets/assets/images/card_images/cards_front/diamond/K.png": "6b5b30c00309e3cfae486f543bc1809a",
"assets/assets/images/card_images/cards_front/diamond/J.png": "d5682eb454510b9cdf54beb9c5a0e5f5",
"assets/assets/images/card_images/cards_front/diamond/8.png": "fcafeaf2d610109aa1916208080ab711",
"assets/assets/images/card_images/cards_front/diamond/9.png": "1d495bb1ebf632dca66a538b61bae19a",
"assets/assets/images/card_images/cards_front/diamond/10.png": "39ef422e15761450c33f8cb3ee369ebe",
"assets/assets/images/card_images/cards_front/diamond/4.png": "89eaac32133444fe40876cb51f697f13",
"assets/assets/images/card_images/cards_front/diamond/5.png": "24fd440cbb52affc5242a507c9dec4d1",
"assets/assets/images/card_images/cards_front/diamond/7.png": "58d872f063752027e59e15af4d090123",
"assets/assets/images/card_images/cards_front/diamond/A.png": "f37d608fb18056bc4f83737d633c5cf5",
"assets/assets/images/card_images/cards_front/diamond/6.png": "ff1c62992cf49b6164401d1d9f77a20c",
"assets/assets/images/card_images/cards_front/diamond/2.png": "1451de5d494406e395215276a2489a7c",
"assets/assets/images/card_images/cards_front/diamond/3.png": "690d5a477dfe9ed93261bd814c0a40d6",
"assets/assets/images/card_images/cards_front/diamond/Q.png": "6940967da8669e3410fefd3a8a33aad9",
"assets/assets/images/card_images/cards_front/club/K.png": "aa73cfd0e548d87f4af4a18a8d2c3c8f",
"assets/assets/images/card_images/cards_front/club/J.png": "1595a3ea21f452c290cf26af7ae53ede",
"assets/assets/images/card_images/cards_front/club/8.png": "a46a54d93ff6e543497d205db97fd460",
"assets/assets/images/card_images/cards_front/club/9.png": "4f8d0d8f2ebaeacf99e7134221d6da49",
"assets/assets/images/card_images/cards_front/club/10.png": "1963502749c024e1590789bab3632bc9",
"assets/assets/images/card_images/cards_front/club/4.png": "23c51e0b449e342f8b7f6c8fd57e2137",
"assets/assets/images/card_images/cards_front/club/5.png": "3ac88eddd1ac03bfc901de76424b5aba",
"assets/assets/images/card_images/cards_front/club/7.png": "4808cc416c976dbd5c3cb629a0f102a5",
"assets/assets/images/card_images/cards_front/club/A.png": "17ca9f77b395a41c6d45cbff350573bb",
"assets/assets/images/card_images/cards_front/club/6.png": "5c96f40f637a6b2ed34d5e837d81ef7b",
"assets/assets/images/card_images/cards_front/club/2.png": "136dab439961d61f4b9c1f939e07828d",
"assets/assets/images/card_images/cards_front/club/3.png": "6ed5bf64f008d72e83c67f81468ab7c5",
"assets/assets/images/card_images/cards_front/club/Q.png": "d6296277472d7e9594d0ebee0cb82cdc",
"assets/assets/images/card_images/cards_front/heart/K.png": "3b48ae8207b07a1f9477d7e6135ca211",
"assets/assets/images/card_images/cards_front/heart/J.png": "fdf4ffc434ac567c6b77905cb1b11c8a",
"assets/assets/images/card_images/cards_front/heart/8.png": "1e9e59b0d6f684908f3ad7d2fe942a42",
"assets/assets/images/card_images/cards_front/heart/9.png": "33ab7891b4259ea8d8823a352ef38cdf",
"assets/assets/images/card_images/cards_front/heart/10.png": "60ab387c8c1c50dd3a75255500218b94",
"assets/assets/images/card_images/cards_front/heart/4.png": "6695f1d514765572dfe7e5dd0863dfce",
"assets/assets/images/card_images/cards_front/heart/5.png": "5457f189cabc0476511c7ed1421b419d",
"assets/assets/images/card_images/cards_front/heart/7.png": "c8475b530ea9f0970ff829c97f3e7abf",
"assets/assets/images/card_images/cards_front/heart/A.png": "a762540d55018bcf43ffba8b6343c9c9",
"assets/assets/images/card_images/cards_front/heart/6.png": "84564e31bf0a0e8bcd5fdd3d4aa12cc3",
"assets/assets/images/card_images/cards_front/heart/2.png": "ebe434953cb5c82ec5c8e38b8e735489",
"assets/assets/images/card_images/cards_front/heart/3.png": "7278d51dda50bd4b8c8cadb7fe349953",
"assets/assets/images/card_images/cards_front/heart/Q.png": "63afa62b47efa84b8b87d3e39ef42bc1",
"assets/assets/images/card_images/cards_front/spade/K.png": "e8d1a4cfe9d8dca64733c050e65e9dfd",
"assets/assets/images/card_images/cards_front/spade/J.png": "89d2c97e62fcaec36c80dbdd725f216f",
"assets/assets/images/card_images/cards_front/spade/8.png": "497eed1efa7e554de5b62bc9eb2b5ae6",
"assets/assets/images/card_images/cards_front/spade/9.png": "50caac183ef66afe6cdda1d2e3daafda",
"assets/assets/images/card_images/cards_front/spade/10.png": "b208cd7f21ce87cf950936ab6fb3e717",
"assets/assets/images/card_images/cards_front/spade/4.png": "5156259e1f30dece1376dc5695a9a1d4",
"assets/assets/images/card_images/cards_front/spade/5.png": "5ab3d8627d0c4d17c86c73d90817900b",
"assets/assets/images/card_images/cards_front/spade/7.png": "82d62864ff67ff7b5e20150316d26872",
"assets/assets/images/card_images/cards_front/spade/A.png": "e6a6d2f8a350079dcad97e814d3559e7",
"assets/assets/images/card_images/cards_front/spade/6.png": "c99b0f04000841e5f3db53d64b3f7034",
"assets/assets/images/card_images/cards_front/spade/2.png": "33c964ae685ff65233d2ac2c35b96072",
"assets/assets/images/card_images/cards_front/spade/3.png": "9638bf9f29919b027765992a81f6d39b",
"assets/assets/images/card_images/cards_front/spade/Q.png": "9026849bcbad6fd92f7c3cb8f70e3cd4",
"assets/assets/images/card_images/cards_back/gray_back.png": "db53954a64b0a647a569a1d3964135ce",
"assets/assets/sounds/error_sound.wav": "7195ed3125db31b648071a1ae2e0d71c",
"assets/assets/sounds/confirm_click_sound.wav": "668417c5a28e5762ab07c7941960c5c9",
"assets/assets/sounds/default_click_sound.wav": "97793a15e18da37ca200181620511610",
"assets/assets/sounds/card_sound.wav": "8ec2319f6fe803fa36852ccca582f0c1",
"assets/assets/fonts/Bradley_Gratis.ttf": "70f929f5d20f8c256cbf09671665b0d0",
"canvaskit/skwasm.js": "1ef3ea3a0fec4569e5d531da25f34095",
"canvaskit/skwasm_heavy.js": "413f5b2b2d9345f37de148e2544f584f",
"canvaskit/skwasm.js.symbols": "0088242d10d7e7d6d2649d1fe1bda7c1",
"canvaskit/canvaskit.js.symbols": "58832fbed59e00d2190aa295c4d70360",
"canvaskit/skwasm_heavy.js.symbols": "3c01ec03b5de6d62c34e17014d1decd3",
"canvaskit/skwasm.wasm": "264db41426307cfc7fa44b95a7772109",
"canvaskit/chromium/canvaskit.js.symbols": "193deaca1a1424049326d4a91ad1d88d",
"canvaskit/chromium/canvaskit.js": "5e27aae346eee469027c80af0751d53d",
"canvaskit/chromium/canvaskit.wasm": "24c77e750a7fa6d474198905249ff506",
"canvaskit/canvaskit.js": "140ccb7d34d0a55065fbd422b843add6",
"canvaskit/canvaskit.wasm": "07b9f5853202304d3b0749d9306573cc",
"canvaskit/skwasm_heavy.wasm": "8034ad26ba2485dab2fd49bdd786837b"};
// The application shell files that are downloaded before a service worker can
// start.
const CORE = ["main.dart.js",
"index.html",
"flutter_bootstrap.js",
"assets/AssetManifest.bin.json",
"assets/FontManifest.json"];

// During install, the TEMP cache is populated with the application shell files.
self.addEventListener("install", (event) => {
  self.skipWaiting();
  return event.waitUntil(
    caches.open(TEMP).then((cache) => {
      return cache.addAll(
        CORE.map((value) => new Request(value, {'cache': 'reload'})));
    })
  );
});
// During activate, the cache is populated with the temp files downloaded in
// install. If this service worker is upgrading from one with a saved
// MANIFEST, then use this to retain unchanged resource files.
self.addEventListener("activate", function(event) {
  return event.waitUntil(async function() {
    try {
      var contentCache = await caches.open(CACHE_NAME);
      var tempCache = await caches.open(TEMP);
      var manifestCache = await caches.open(MANIFEST);
      var manifest = await manifestCache.match('manifest');
      // When there is no prior manifest, clear the entire cache.
      if (!manifest) {
        await caches.delete(CACHE_NAME);
        contentCache = await caches.open(CACHE_NAME);
        for (var request of await tempCache.keys()) {
          var response = await tempCache.match(request);
          await contentCache.put(request, response);
        }
        await caches.delete(TEMP);
        // Save the manifest to make future upgrades efficient.
        await manifestCache.put('manifest', new Response(JSON.stringify(RESOURCES)));
        // Claim client to enable caching on first launch
        self.clients.claim();
        return;
      }
      var oldManifest = await manifest.json();
      var origin = self.location.origin;
      for (var request of await contentCache.keys()) {
        var key = request.url.substring(origin.length + 1);
        if (key == "") {
          key = "/";
        }
        // If a resource from the old manifest is not in the new cache, or if
        // the MD5 sum has changed, delete it. Otherwise the resource is left
        // in the cache and can be reused by the new service worker.
        if (!RESOURCES[key] || RESOURCES[key] != oldManifest[key]) {
          await contentCache.delete(request);
        }
      }
      // Populate the cache with the app shell TEMP files, potentially overwriting
      // cache files preserved above.
      for (var request of await tempCache.keys()) {
        var response = await tempCache.match(request);
        await contentCache.put(request, response);
      }
      await caches.delete(TEMP);
      // Save the manifest to make future upgrades efficient.
      await manifestCache.put('manifest', new Response(JSON.stringify(RESOURCES)));
      // Claim client to enable caching on first launch
      self.clients.claim();
      return;
    } catch (err) {
      // On an unhandled exception the state of the cache cannot be guaranteed.
      console.error('Failed to upgrade service worker: ' + err);
      await caches.delete(CACHE_NAME);
      await caches.delete(TEMP);
      await caches.delete(MANIFEST);
    }
  }());
});
// The fetch handler redirects requests for RESOURCE files to the service
// worker cache.
self.addEventListener("fetch", (event) => {
  if (event.request.method !== 'GET') {
    return;
  }
  var origin = self.location.origin;
  var key = event.request.url.substring(origin.length + 1);
  // Redirect URLs to the index.html
  if (key.indexOf('?v=') != -1) {
    key = key.split('?v=')[0];
  }
  if (event.request.url == origin || event.request.url.startsWith(origin + '/#') || key == '') {
    key = '/';
  }
  // If the URL is not the RESOURCE list then return to signal that the
  // browser should take over.
  if (!RESOURCES[key]) {
    return;
  }
  // If the URL is the index.html, perform an online-first request.
  if (key == '/') {
    return onlineFirst(event);
  }
  event.respondWith(caches.open(CACHE_NAME)
    .then((cache) =>  {
      return cache.match(event.request).then((response) => {
        // Either respond with the cached resource, or perform a fetch and
        // lazily populate the cache only if the resource was successfully fetched.
        return response || fetch(event.request).then((response) => {
          if (response && Boolean(response.ok)) {
            cache.put(event.request, response.clone());
          }
          return response;
        });
      })
    })
  );
});
self.addEventListener('message', (event) => {
  // SkipWaiting can be used to immediately activate a waiting service worker.
  // This will also require a page refresh triggered by the main worker.
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
    return;
  }
  if (event.data === 'downloadOffline') {
    downloadOffline();
    return;
  }
});
// Download offline will check the RESOURCES for all files not in the cache
// and populate them.
async function downloadOffline() {
  var resources = [];
  var contentCache = await caches.open(CACHE_NAME);
  var currentContent = {};
  for (var request of await contentCache.keys()) {
    var key = request.url.substring(origin.length + 1);
    if (key == "") {
      key = "/";
    }
    currentContent[key] = true;
  }
  for (var resourceKey of Object.keys(RESOURCES)) {
    if (!currentContent[resourceKey]) {
      resources.push(resourceKey);
    }
  }
  return contentCache.addAll(resources);
}
// Attempt to download the resource online before falling back to
// the offline cache.
function onlineFirst(event) {
  return event.respondWith(
    fetch(event.request).then((response) => {
      return caches.open(CACHE_NAME).then((cache) => {
        cache.put(event.request, response.clone());
        return response;
      });
    }).catch((error) => {
      return caches.open(CACHE_NAME).then((cache) => {
        return cache.match(event.request).then((response) => {
          if (response != null) {
            return response;
          }
          throw error;
        });
      });
    })
  );
}
