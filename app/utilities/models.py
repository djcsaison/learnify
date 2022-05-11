from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field
import pydantic


class PennyTesting(BaseModel):
    validationId: str
    debitAccountNumber: str
    accountNumber: str
    appFormId: str
    accountStatus: str
    utr: str
    registeredName: str
    failureReason: Any
    serviceProvider: str
    name: str
    id: str
    ifsc: str
    email: str
    status: str


class CreditPolicyCheck(BaseModel):
    income: str
    pincode: str
    salaryType: str
    age: str


class OfferSection(BaseModel):
    income: str
    validTill: str
    foir: str
    interest: str
    limitAmount: str
    id: str
    ksfScore: str
    tenure: str
    segmentName: str
    status: str


class InitialOffer(BaseModel):
    remarks: List
    status: str
    offerSection: OfferSection


class OfferSection1(BaseModel):
    income: str
    minWithdrwalAmount: str
    validTill: str
    foir: str
    ksfScore: str
    segmentName: str
    maxTenure: str
    interest: str
    limitAmount: str
    id: str
    minTenure: str
    bankStatementScore: str
    status: str


class FinalOffer(BaseModel):
    remarks: List
    salaryDay: str
    status: str
    offerSection: OfferSection1


class CurrentWithdrawal(BaseModel):
    bpiAmount: str
    disbursalAmount: str
    reason: Any
    withdrawalId: str
    utr: str
    partnerLoanId: str
    loanIntRate: str
    withdrawalStatus: str
    withdrawalStatusCode: str
    loanAmount: str
    tenure: str
    processingFee: str


class Verification(BaseModel):
    pan: str
    employment: str


class InternalDedupeItem(BaseModel):
    applicantId: str
    dedupeStatus: str
    dedupeReason: str


class Applicant(BaseModel):
    income: str
    firstName: str
    phoneNumber: str
    workEmail: str
    pennantCif: str
    customerId: str
    fullName: str
    employerName: str
    pennantError: Any
    applicantId: str
    type: str
    personalEmail: str


class Preprocessor(BaseModel):
    hard_bureau: str
    customer_device_details: str
    selfie: str
    aadhar: str
    aadhaar: str
    credit_vidhya: str
    sherlock: str
    ckyc: str
    karza_employment: str
    perfios: str
    pan_karza: str


class PerfiosAccountDetails(BaseModel):
    account_number_masked: bool
    ifsc_code: Any
    account_number: str
    ifsc_code_masked: bool
    account_type: str
    report_id: str


class ESignResponse(BaseModel):
    appFormId: str
    tokenId: str
    documentId: str


class Item(BaseModel):
    perfiosStatus: str
    loanProduct: str
    status: str
    fraudCheckResponse: str
    pennyTesting: PennyTesting
    creditPolicyCheck: CreditPolicyCheck
    eSign: str
    initialOffer: InitialOffer
    finalOffer: FinalOffer
    finalOfferStatus: str
    selfie: str
    state: str
    mandateStatus: str
    currentWithdrawal: CurrentWithdrawal
    verification: Verification
    pennyTestingStatus: str
    internalDedupe: List[InternalDedupeItem]
    applicant: Applicant
    preprocessor: Preprocessor
    appFormId: str
    interestRate: str
    fraudCheckStatus: str
    perfiosAccountDetails: PerfiosAccountDetails
    createdAt: str
    comments: Any
    creditLimit: str
    updatedAt: str
    eSignResponse: ESignResponse
    description: str
    initialOfferStatus: str


class HTTPHeaders(BaseModel):
    server: str
    date: str
    content_type: str = Field(..., alias='content-type')
    content_length: str = Field(..., alias='content-length')
    connection: str
    x_amzn_requestid: str = Field(..., alias='x-amzn-requestid')
    x_amz_crc32: str = Field(..., alias='x-amz-crc32')


class ResponseMetadata(BaseModel):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: HTTPHeaders
    RetryAttempts: int


class Model(BaseModel):
    Item: Optional[Item] = None
    #ResponseMetadata: Optional[ResponseMetadata] = None

class AllOptional(pydantic.main.ModelMetaclass):
    def __new__(self, name, bases, namespaces, **kwargs):
        annotations = namespaces.get('__annotations__', {})
        for base in bases:
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith('__'):
                annotations[field] = Optional[annotations[field]]
        namespaces['__annotations__'] = annotations
        return super().__new__(self, name, bases, namespaces, **kwargs)