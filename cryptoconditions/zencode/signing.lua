-- Signing Scenario

load_scenario("general")

local KEYRING = import("keyring")
local JSON = import("json")
local OCTET = import("octet")

local new_keyring = function(name)
    ACK[name] = KEYRING.new()
end

Given("a blank keyring", function()
    new_keyring("keyring")
end)


local gen_key = function(name)
    ACK[name]:generate()
end

Then("generate a new key pair", function()
    gen_key("keyring")
end)


local serialize_key = function(from, to)
    local keyring = ACK[from]
    ACK[to] = {
        public = keyring:public():base64(),
        private = keyring:private():base64()
    }
end

Then("serialize my keyring", function()
    serialize_key("keyring", "serialized_keyring")
end)

local load_private_key = function(keyring_name, name)
    local serialized_keyring = JSON.decode(IN.KEYS[name])
    ACK[keyring_name]:private(OCTET.base64(serialized_keyring.private))
end

Then("load my serialized private key", function()
    load_private_key("keyring", ACK.WHOAMI)
end)

local load_public_key = function(keyring_name, name)
    local serialized_keyring = JSON.decode(IN.KEYS[name])
    ACK[keyring_name]:public(OCTET.base64(serialized_keyring.public))
end

local load_constant_public_key = function(keyring_name, name)
    public_key = OCTET.base64(ACK[name])
    ACK[keyring_name]:public(public_key)
end

Then("load my serialized public key", function()
    load_public_key("keyring", ACK.WHOAMI)
end)

Then("load serialized public key from ''", function(name)
    load_constant_public_key("keyring", name)
end)

local sign_message = function(keyring_name, input, out)
    local keyring = ACK[keyring_name]
    ACK[out] = keyring:sign(ACK[input])
end

Then("sign ''", function(input)
    sign_message("keyring", input, "signature")
end)

local verify_signature = function(keyring_name, message, signature, out)
    local keyring = ACK[keyring_name]
    ACK[out] = keyring:verify(ACK[message], ACK[signature])
end

Then("verify the signature for ''", function(message)
    verify_signature("keyring", message, "signature", "verified")
end)
