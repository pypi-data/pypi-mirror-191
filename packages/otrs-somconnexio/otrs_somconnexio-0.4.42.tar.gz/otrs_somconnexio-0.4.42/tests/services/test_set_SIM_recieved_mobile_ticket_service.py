import unittest

from mock import ANY, Mock, call, patch
from datetime import date

from otrs_somconnexio.services.set_SIM_recieved_mobile_ticket import \
    SetSIMRecievedMobileTicket


class SetSIMRecievedMobileTicketTestCase(unittest.TestCase):

    @patch('otrs_somconnexio.services.set_SIM_recieved_mobile_ticket.date')
    @patch(
        "otrs_somconnexio.services.update_ticket_DF_if_not_set.OTRSClient",
        return_value=Mock(
            spec=[
                "update_ticket_if_not_set",
                "get_ticket_by_number",
            ]
        ),
    )
    @patch("otrs_somconnexio.services.set_SIM_recieved_mobile_ticket.DynamicField")
    def test_run_create_ended_fiber(self, MockDF, MockOTRSClient, MockDate):
        ticket_number = "123"
        expected_df = object()
        MockDF.return_value = expected_df
        MockOTRSClient.return_value.get_ticket_by_number.return_value = Mock(
            spec=["tid", "field_get"]
        )
        MockOTRSClient.return_value.get_ticket_by_number.return_value.tid = 321
        MockOTRSClient.return_value.get_ticket_by_number.return_value.field_get.return_value = "Serveis mòbil::Provisió mòbil::01.1 Fibra finalitzada"
        MockDate.today.return_value = date(2023,1,11)
        response = SetSIMRecievedMobileTicket(ticket_number, True).run()
        self.assertEqual(response, date(2023,1,18)) 
        MockOTRSClient.return_value.get_ticket_by_number.assert_called_once_with(
            ticket_number,
            dynamic_fields=True,
        )
        MockOTRSClient.return_value.update_ticket_if_not_set.assert_called_once_with(
            MockOTRSClient.return_value.get_ticket_by_number.return_value.tid,
            article=None,
            dynamic_fields=[expected_df] * 3
        )
        MockDF.assert_has_calls([
            call(
                name="SIMrebuda",
                value=1,
            ),
            call(
                name='dataActivacioLiniaMobil',
                value='2023-01-19'
            ),
            call(
                name='dataIntroPlataforma',
                value='2023-01-17'
            )
        ])

    @patch('otrs_somconnexio.services.set_SIM_recieved_mobile_ticket.date')
    @patch(
        "otrs_somconnexio.services.update_ticket_DF_if_not_set.OTRSClient",
        return_value=Mock(
            spec=[
                "update_ticket_if_not_set",
                "get_ticket_by_number",
            ]
        ),
    )
    @patch("otrs_somconnexio.services.set_SIM_recieved_mobile_ticket.DynamicField")
    def test_run_pack(self, MockDF, MockOTRSClient, MockDate):
        ticket_number = "123"
        expected_df = object()
        MockDF.return_value = expected_df
        MockOTRSClient.return_value.get_ticket_by_number.return_value = Mock(
            spec=["tid", "field_get"]
        )
        MockOTRSClient.return_value.get_ticket_by_number.return_value.tid = 321
        MockOTRSClient.return_value.get_ticket_by_number.return_value.field_get.return_value = "XXX"
        MockDate.today.return_value = date(2023,1,11)
        response = SetSIMRecievedMobileTicket(ticket_number, True).run()
        self.assertFalse(response) 
        MockOTRSClient.return_value.get_ticket_by_number.assert_called_once_with(
            ticket_number,
            dynamic_fields=True,
        )
        MockOTRSClient.return_value.update_ticket_if_not_set.assert_called_once_with(
            MockOTRSClient.return_value.get_ticket_by_number.return_value.tid,
            article=None,
            dynamic_fields=[expected_df]
        )
        MockDF.assert_has_calls([
            call(
                name="SIMrebuda",
                value=1,
            )
        ])

    @patch('otrs_somconnexio.services.set_SIM_recieved_mobile_ticket.date')
    @patch(
        "otrs_somconnexio.services.update_ticket_DF_if_not_set.OTRSClient",
        return_value=Mock(
            spec=[
                "update_ticket_if_not_set",
                "get_ticket_by_number",
            ]
        ),
    )
    @patch("otrs_somconnexio.services.set_SIM_recieved_mobile_ticket.DynamicField")
    def test_run_no_confirm_doc(self, MockDF, MockOTRSClient, MockDate):
        ticket_number = "123"
        expected_df = object()
        MockDF.return_value = expected_df
        MockOTRSClient.return_value.get_ticket_by_number.return_value = Mock(
            spec=["tid", "field_get", "dynamic_field_get"]
        )
        MockOTRSClient.return_value.get_ticket_by_number.return_value.tid = 321
        MockOTRSClient.return_value.get_ticket_by_number.return_value.field_get.return_value = "XXX"
        MockOTRSClient.return_value.get_ticket_by_number.return_value.dynamic_field_get.return_value = "no"
        MockDate.today.return_value = date(2023,1,11)
        response = SetSIMRecievedMobileTicket(ticket_number, False).run()
        self.assertFalse(response) 
        MockOTRSClient.return_value.get_ticket_by_number.assert_called_once_with(
            ticket_number,
            dynamic_fields=True,
        )
        MockOTRSClient.return_value.update_ticket_if_not_set.assert_called_once_with(
            MockOTRSClient.return_value.get_ticket_by_number.return_value.tid,
            article=None,
            dynamic_fields=[expected_df]
        )
        MockDF.assert_has_calls([
            call(
                name="SIMrebuda",
                value=1,
            )
        ])

    @patch('otrs_somconnexio.services.set_SIM_recieved_mobile_ticket.date')
    @patch(
        "otrs_somconnexio.services.update_ticket_DF_if_not_set.OTRSClient",
        return_value=Mock(
            spec=[
                "update_ticket_if_not_set",
                "get_ticket_by_number",
            ]
        ),
    )
    @patch("otrs_somconnexio.services.set_SIM_recieved_mobile_ticket.DynamicField")
    def test_run_confirm_doc(self, MockDF, MockOTRSClient, MockDate):
        ticket_number = "123"
        expected_df = object()
        MockDF.return_value = expected_df
        MockOTRSClient.return_value.get_ticket_by_number.return_value = Mock(
            spec=["tid", "field_get", "dynamic_field_get"]
        )
        MockOTRSClient.return_value.get_ticket_by_number.return_value.tid = 321
        MockOTRSClient.return_value.get_ticket_by_number.return_value.field_get.return_value = "XXX"
        MockOTRSClient.return_value.get_ticket_by_number.return_value.dynamic_field_get.return_value = "si"
        MockDate.today.return_value = date(2023,1,11)
        response = SetSIMRecievedMobileTicket(ticket_number, False).run()
        self.assertEqual(response, date(2023,1,18)) 
        MockOTRSClient.return_value.get_ticket_by_number.assert_called_once_with(
            ticket_number,
            dynamic_fields=True,
        )
        MockOTRSClient.return_value.update_ticket_if_not_set.assert_called_once_with(
            MockOTRSClient.return_value.get_ticket_by_number.return_value.tid,
            article=None,
            dynamic_fields=[expected_df] * 3
        )
        MockDF.assert_has_calls([
            call(
                name="SIMrebuda",
                value=1,
            ),
            call(
                name='dataActivacioLiniaMobil',
                value='2023-01-19'
            ),
            call(
                name='dataIntroPlataforma',
                value='2023-01-17'
            )
        ])
