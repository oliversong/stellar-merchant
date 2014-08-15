function Astral(auth_token) {
  this.auth_token = auth_token;
}

Astral.prototype.payWithAstral = function(price) {
  // redirect to Astral with params
  window.location.href = "http://localhost:5000/pay?auth_token="+ encodeURIComponent(this.auth_token) + "&price="+ encodeURIComponent(price);
};

Astral.prototype.buyAstralGiftCard = function(id) {
  // redirect to Astral with params
  window.location.href = "http://localhost:5000/gift?auth_token=" + encodeURIComponent(this.auth_token) + "&gcid="+ encodeURIComponent(id);
};
