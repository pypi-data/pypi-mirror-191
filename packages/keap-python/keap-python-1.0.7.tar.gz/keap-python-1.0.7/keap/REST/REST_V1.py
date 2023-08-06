from keap.REST.V1 import (
    AccountService, AffiliateService, AppointmentService, CampaignService, CompanyService,
    ContactService, EmailService, FileService, HookService, LocaleService, MerchantService, NoteService, OpportunityService,
    OrderService, ProductService, SettingService, SubscriptionService, TagService, TaskService, TransactionService,
    UserService)


class REST_V1:
    def __init__(self, keap):
        self.keap = keap
        self.AccountService = AccountService(keap)
        self.AffiliateService = AffiliateService(keap)
        self.AppointmentService = AppointmentService(keap)
        self.CampaignService = CampaignService(keap)
        self.CompanyService = CompanyService(keap)
        self.ContactService = ContactService(keap)
        self.EmailService = EmailService(keap)
        self.FileService = FileService(keap)
        self.HookService = HookService(keap)
        self.LocaleService = LocaleService(keap)
        self.MerchantService = MerchantService(keap)
        self.NoteService = NoteService(keap)
        self.OpportunityService = OpportunityService(keap)
        self.OrderService = OrderService(keap)
        self.ProductService = ProductService(keap)
        self.SettingService = SettingService(keap)
        self.SubscriptionService = SubscriptionService(keap)
        self.TagService = TagService(keap)
        self.TaskService = TaskService(keap)
        self.TransactionService = TransactionService(keap)
        self.UserService = UserService(keap)

    def test_connection(self):
        return self.SettingService.get_application_status()
