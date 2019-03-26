--
-- Created by IntelliJ IDEA.
-- User: fanwei.zeng
-- Date: 2019/3/22
-- Time: 6:11 PM
-- To change this template use File | Settings | File Templates.
--
redis.replicate_commands()

local function now()
    local ts = redis.call('TIME')
    return tostring(ts[1] + ts[2] / 1000000)
end

local Funnel = {}

function Funnel:new(o, capacity, operations, seconds, left_quota, leaking_ts)
    o = o or {}
    setmetatable(o, self)
    self.__index = self
    self.capacity = capacity
    self.operations = operations
    self.seconds = seconds
    self.left_quota = left_quota
    self.leaking_ts = leaking_ts
    self.leaking_rate = operations / seconds
    return o
end

function Funnel:make_space(quota)
    local now_ts = now()
    local delta_ts = now_ts - self.leaking_ts
    local delta_quota = delta_ts * self.leaking_rate
    if (self.left_quota + delta_quota) < quota then
        return
    else
        self.left_quota = self.left_quota + delta_quota
        if self.left_quota > self.capacity then
            self.left_quota = self.capacity
        end
        self.leaking_ts = now_ts
    end
end

function Funnel:watering(quota)
    self:make_space(quota)
    if self.left_quota >= quota then
        self.left_quota = self.left_quota - quota
        return
            0,
            self.capacity,
            self.left_quota,
            tostring(-1.0),
            tostring((self.capacity - self.left_quota) / self.leaking_rate)
    else
        return
            1,
            self.capacity,
            self.left_quota,
            tostring(quota / self.leaking_rate),
            tostring((self.capacity - self.left_quota) / self.leaking_rate)
    end
end

local group = KEYS[1]
local key = KEYS[1] .. ':' .. KEYS[2]
local capacity = tonumber(ARGV[1])
local operations = tonumber(ARGV[2])
local seconds = tonumber(ARGV[3])
local quota = tonumber(ARGV[4])

local left_quota
local leaking_ts
local cache = redis.call('HMGET', key, 'left_quota', 'leaking_ts')
if cache[1] ~= false then
    left_quota = tonumber(cache[1])
    if left_quota > capacity then
        left_quota = capacity
    end
    leaking_ts = cache[2]
else
    left_quota = 0
    leaking_ts = now()
end

local funnel = Funnel:new(nil, capacity, operations, seconds, left_quota, leaking_ts)
local ready, capacity, left_quota, interval, empty_time = funnel:watering(quota)

redis.call('HMSET', key,
    'left_quota', funnel.left_quota,
    'leaking_ts', funnel.leaking_ts,
    'capacity', funnel.capacity,
    'operations', funnel.operations,
    'seconds', funnel.seconds
)
redis.call('SADD', 'funnel:groups', group)
redis.call('SADD', 'funnel:' .. group .. ':keys', key)

return {ready, capacity, left_quota, interval, empty_time}