# kmymoney-stock-server
A simple http server to be a single Online Quote Source for stock market info for KMyMoney.


## Online Quote Sources
Add the below sources to the `kmymoneyrc` file.

```
[Online-Quote-Source-# Localhost BR Stock]
DateFormatRegex=%y-%m-%d
DateRegex=([0-9]{4}-[0-9]{2}-[0-9]{2})
PriceRegex=([0-9]+\\.[0-9]+)
SymbolRegex=
URL=http://localhost:1203/stock/br/%1

[Online-Quote-Source-# Localhost Currency]
DateFormatRegex=%y-%m-%d
DateRegex=([0-9]{4}-[0-9]{2}-[0-9]{2})
PriceRegex=([0-9]+\\.[0-9]+)
SymbolRegex=
URL=http://localhost:1203/currency/%1%2

[Online-Quote-Source-# Localhost USA Stock]
DateFormatRegex=%y-%m-%d
DateRegex=([0-9]{4}-[0-9]{2}-[0-9]{2})
PriceRegex=([0-9]+\\.[0-9]+)
SymbolRegex=
URL=http://localhost:1203/stock/usa/%1
```

## Run server
`python2 "./stock-server.py"`