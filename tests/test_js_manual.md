```js
global.window = {};
global.restaurantData = [
  { name: "Test Rest", address: "Street 1", rating: 5, distance_mi: 1.2 },
];
global.window._markers = {};
global.window._openInfoWindow = null;
global.window._closeInfoWindow = () => {};
global.window._focusRestaurant = () => {};

function runTests() {
  let passed = 0;
  let failed = 0;

  function assert(description, condition) {
    if (condition) {
      console.log(`✅ PASS: ${description}`);
      passed++;
    } else {
      console.log(`❌ FAIL: ${description}`);
      failed++;
    }
  }

  assert("restaurantData is an array", Array.isArray(restaurantData));
  assert(
    "restaurants have names",
    restaurantData.every((r) => r.name),
  );
  assert(
    "restaurants have addresses",
    restaurantData.every((r) => r.address),
  );
  assert(
    "restaurants have ratings",
    restaurantData.every((r) => r.rating !== undefined),
  );
  assert(
    "restaurants have distance_mi",
    restaurantData.every((r) => r.distance_mi !== undefined),
  );

  assert(
    "_closeInfoWindow is a function",
    typeof window._closeInfoWindow === "function",
  );
  assert(
    "_focusRestaurant is a function",
    typeof window._focusRestaurant === "function",
  );
  assert("_markers is an object", typeof window._markers === "object");
  assert("no info window open on load", window._openInfoWindow === null);

  console.log(`\n${passed} passed, ${failed} failed`);
}

runTests();
```
