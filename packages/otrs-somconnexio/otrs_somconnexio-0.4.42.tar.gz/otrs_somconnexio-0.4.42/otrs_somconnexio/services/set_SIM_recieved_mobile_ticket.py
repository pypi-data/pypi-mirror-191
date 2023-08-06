# coding: utf-8
from pyotrs.lib import DynamicField
from datetime import date, timedelta
from .update_ticket_DF_if_not_set import UpdateTicketDFIfNotSet


class SetSIMRecievedMobileTicket(UpdateTicketDFIfNotSet):
    """
    Set DF SImRebuda to True to OTRS mobile tickets.
    """
    def __init__(self, ticket_number, is_pack):
        self.is_pack = is_pack
        self.scheduled_activation = False
        super().__init__(ticket_number)

    def _get_response(self):
        return self.scheduled_activation

    def _prepare_dynamic_fields(self, ticket):
        today = date.today()
        mobile_line_activation_date = today + timedelta(days=8)
        num_days = 0
        days_decrement = 0
        while num_days < 2:
            if (
                mobile_line_activation_date - timedelta(days=days_decrement)
            ).weekday() < 5:
                num_days += 1
            days_decrement += 1
        platform_intro_date = (
            mobile_line_activation_date - timedelta(days=days_decrement)
        )
        if ticket.field_get('Queue') == (
            'Serveis mòbil::Provisió mòbil::01.1 Fibra finalitzada'
        ):
            self.scheduled_activation = today + timedelta(days=7)
            return [
                DynamicField(name='SIMrebuda', value=1),
                DynamicField(
                    name='dataActivacioLiniaMobil',
                    value=str(mobile_line_activation_date)
                ),
                DynamicField(
                    name='dataIntroPlataforma',
                    value=str(platform_intro_date)
                ),
            ]
        else:
            if self.is_pack:
                return [
                    DynamicField(name='SIMrebuda', value=1)
                ]
            else:
                if ticket.dynamic_field_get('confirmDoc') == "si":
                    self.scheduled_activation = today + timedelta(days=7)
                    return [
                        DynamicField(name='SIMrebuda', value=1),
                        DynamicField(
                            name='dataActivacioLiniaMobil',
                            value=str(mobile_line_activation_date)
                        ),
                        DynamicField(
                            name='dataIntroPlataforma',
                            value=str(platform_intro_date)
                        ),
                    ]
                else:
                    return [
                        DynamicField(name='SIMrebuda', value=1)
                    ]
