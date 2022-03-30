from abc import abstractmethod
from dataclasses import dataclass
from abc import ABC

from pkg.comm.Currency import Currency


class BankingRequest(ABC):
    pass

@dataclass
class OpenAccountRequest(BankingRequest):
    name: str
    password: str
    currency: Currency
    balance: int

@dataclass
class CloseAccountRequest(BankingRequest):
    name: str
    accountNumber: int
    password: str

@dataclass
class QueryAccountRequest(BankingRequest):
    accountNumber: int
    password: str

@dataclass
class DepositAccountRequest(BankingRequest):
    name: str
    accountNumber: int
    password: str
    currency: Currency
    amonunt: int

@dataclass
class MaintenanceFeeAccountRequest(BankingRequest):
    accountNumber: int
    name: str
    password: str

@dataclass
class MonitorAccountRequest(BankingRequest):
    ipAddress: str
    port: int
    interval: int
