mkdir AribaCarDealership
cd AribaCarDealership

dotnet new sln -n AribaCarDealership

# Core projects
dotnet new classlib -n AribaCarDealership.Domain
dotnet new classlib -n AribaCarDealership.Application

# Infrastructure projects
dotnet new classlib -n AribaCarDealership.Infrastructure
dotnet new classlib -n AribaCarDealership.Persistence

# Presentation projects
dotnet new wpf -n AribaCarDealership.WPF
dotnet new winforms -n AribaCarDealership.WinForms
dotnet new maui -n AribaCarDealership.MAUI

# Add projects to solution
dotnet sln add AribaCarDealership.Domain
dotnet sln add AribaCarDealership.Application
dotnet sln add AribaCarDealership.Infrastructure
dotnet sln add AribaCarDealership.Persistence
dotnet sln add AribaCarDealership.WPF
dotnet sln add AribaCarDealership.WinForms
dotnet sln add AribaCarDealership.MAUI