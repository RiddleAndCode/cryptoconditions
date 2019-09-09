-- General Scenario

load_scenario("encoding")

local write_to_ack = function(from, to)
    ACK[to] = IN[from]
end

Given("the input '' as ''", write_to_ack)
Given("the input ''", function(name)
    write_to_ack(name, name)
end)
Given("the constant '' is ''", function(to, constant)
    ACK[to] = constant
end)


local write_to_out = function(from, to)
    OUT[to] = ACK[from]
end

Then("return '' as ''", write_to_out)
Then("return ''", function(name)
    write_to_out(name, name)
end)

Then("assert ''", function(name)
    assert(ACK[name])
end)

Then("assert not ''", function(name)
    assert(not ACK[name])
end)


local mark_identity = function(name)
    ACK.WHOAMI = name
end

Given("that I am ''", mark_identity)
