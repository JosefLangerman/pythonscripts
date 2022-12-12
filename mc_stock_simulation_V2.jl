using CSV
using DataFrames
using Plots
using Statistics


""" We are simulting montly stock gen_paths"""
function gen_paths(N,M, S0, r, sigma)
    #
    dt = 1.0/12 #Monthly steps 
    ZMatrix = randn((N, M + 1))
    S = S0 .* exp.(cumsum((r - 0.5*sigma^2) * dt .+ sigma * sqrt(dt) * ZMatrix, dims=2))
    S[1:end,1] .= S0
    return S
end

"""Quick function for computing relative returns"""
get_rel_returns(pvec) = diff((pvec))./pvec[1:end-1]

"""#Get Data Source """
filepath = "C:\\Users\\hadonfack\\Documents\\Projects\\2019\\LiabilityDrivenInvestment\\Josef\\Julia"
#
price_df = CSV.read(filepath*"\\prices.csv",DataFrame)
close_prices = reverse(price_df[: ,5]) # Origimnal data were from recent to oldest
log_ret = diff(log.(close_prices))
rel_ret = get_rel_returns(close_prices)
#
#plot(log_ret, title = "S&P500 returns", legend = true)
#plot!(rel_ret, title = "S&P500 returns", legend = true)
#
#histogram(log_ret, bins = :scott)
#histogram(rel_ret, bins = :scott)

# compute \mu   and \sigma 
μlog = mean(log_ret)*12
μ = mean(rel_ret)*12
#
σlog = std(log_ret)*sqrt(12)
σ = std(rel_ret)*sqrt(12)
#
#spot = close_prices[end]
spot = close_prices[1]
#
npaths = 1000000
nsteps = 143  

store =[]

listofsample=[100, 1000, 5000, 10000, 30000, 50000, 70000, 100000, 300000, 500000, 1000000]
for np in listofsample
    spathslog = gen_paths(np, nsteps,spot, μlog, σlog)
    meanlog = mean(spathslog[:,end])
    append!(store, meanlog)
end

expected = spot*exp(μlog*144/12)

scatter(listofsample,store)
hline!([expected])
spaths = gen_paths(npaths, nsteps,spot, μ, σ)

"""Visualization of paths"""
time_axis = LinRange(0, nsteps,nsteps+1)

returns_meanpath = mean(spaths,dims=1)[1,:]

first_quantile = [quantile(spaths[:,i], 0.25) for i in 1:nsteps+1]
second_quantile = [quantile(spaths[:,i], 0.5) for i in 1:nsteps+1]
third_quantile = [quantile(spaths[:,i], 0.75) for i in 1:nsteps+1]

#plot(time_axis,returns_meanpath, lw=4)
#plot()
#plot!(time_axis, first_quantile, lw=4)
#plot!(time_axis, second_quantile, lw=4)
#plot!(time_axis, third_quantile, lw=4)
#for i in 50:70
#    display(plot!(time_axis,spaths[i,:], legend = false, xlabel="T", ylabel="Price"))
#end

#mc_log_ret = diff(log.(meanpath[1,:]))
mc_rel_ret = get_rel_returns(returns_meanpath)
μ_mc = mean(mc_rel_ret)*12
#plot(mc_rel_ret )

mean(spaths[:,end])
μ
expected = spot*exp(μlog*143/12)