// Each language link points to the corresponding page, including manual chapters.
// Keep links from the former one-page guide useful after the page split.
const legacyRoutes = document.getElementById('legacy-routes');
if (legacyRoutes && location.hash) {
  const route = JSON.parse(legacyRoutes.textContent)[location.hash.slice(1)];
  if (route) location.replace(new URL(route, location.href));
}
