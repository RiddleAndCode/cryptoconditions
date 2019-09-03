-- Encoding scenario

local OCTET = import("octet")

decode_base64 = function(from, to)
    ACK[to] = OCTET.base64(ACK[from])
end

encode_base64 = function(from, to)
    ACK[to] = ACK[from]:base64()
end

decode_string = function(from, to)
    ACK[to] = OCTET.string(ACK[from])
end

encode_string = function(from, to)
    ACK[to] = ACK[from]:string()
end


Then("decode base64 ''", function(name)
    decode_base64(name, name)
end)

Then("encode base64 ''", function(name)
    encode_base64(name, name)
end)

Then("decode ''", function(name)
    decode_string(name, name)
end)

Then("encode ''", function(name)
    encode_string(name, name)
end)
