import unittest
from index import to_string, to_array_of_plain_strings_or_json, first_json, last_json, largest_json, json_matching
import json
import re

class TestParseJson(unittest.TestCase):

    def assert_is_json(self, json_string):
        try:
            json.loads(json_string)
            return True
        except ValueError:
            return False

    def test_to_string_function_exists(self):
        self.assertIsNotNone(to_string)

    def test_should_return_valid_json_string_from_inspected_output(self):
        input = "{ test: 'test', array: ['test', { test: 'test' }] }"
        result = to_string(input)
        expected = '{ "test": "test", "array": ["test", { "test": "test" }] }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_return_array_of_strings_and_json_strings(self):
        input = "text before { test: 'test', array: ['test', { test: 'test' }] } text after"
        result = to_array_of_plain_strings_or_json(input)
        self.assertEqual(result[0], 'text before ')
        self.assertEqual(result[1], '{ "test": "test", "array": ["test", { "test": "test" }] }')
        self.assertEqual(result[2], ' text after')
        self.assertTrue(self.assert_is_json(result[1]))

    def test_should_return_first_valid_json_object(self):
        input = "text before { test: 'test', array: ['test', { test: 'test' }] } text { hey: 1 } after"
        result = first_json(input)
        expected = '{ "test": "test", "array": ["test", { "test": "test" }] }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_return_last_valid_json_object(self):
        input = "text before { test: 'test', array: ['test', { test: 'test' }] } text { hey: 1 } after"
        result = last_json(input)
        expected = '{ "hey": 1 }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_return_largest_valid_json_object(self):
        input = "text { gday: 'hi' } before { test: 'test', array: ['test', { test: 'test' }] } text { hey: 1 } after"
        result = largest_json(input)
        expected = '{ "test": "test", "array": ["test", { "test": "test" }] }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_return_json_object_matching_regular_expression(self):
        input = "text { gday: 'hi' } before { test: 'test', array: ['test', { test: 'test' }] } text { hey: 1 } after"
        pattern = re.compile("hey")
        result = json_matching(input, pattern)
        expected = '{ "hey": 1 }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_brace_in_string(self):
        input = 'real json {"value":["closing brace }"]}'
        result = to_array_of_plain_strings_or_json(input)
        self.assertEqual(result[0], 'real json ')
        self.assertEqual(result[1], '{ "value": ["closing brace }"] }')
        self.assertTrue(self.assert_is_json(result[1]))

    def test_should_cope_with_double_quote_in_string(self):
        input = 'real json {"value":["double quote \\"test"]}'
        result = to_array_of_plain_strings_or_json(input)
        self.assertEqual(result[0], 'real json ')
        self.assertEqual(result[1], '{ "value": ["double quote \\"test"] }')
        self.assertTrue(self.assert_is_json(result[1]))

    def test_should_parse_an_array_of_numbers(self):
        input = 'real json { "test": [ 1, 2, 3] }'
        result = to_array_of_plain_strings_or_json(input)
        self.assertEqual(result[0], 'real json ')
        self.assertEqual(result[1], '{ "test": [1, 2, 3] }')
        self.assertTrue(self.assert_is_json(result[1]))

    def test_should_cope_with_empty_object(self):
        input = 'is json {} abc'
        result = to_array_of_plain_strings_or_json(input)
        self.assertEqual(result[0], 'is json ')
        self.assertEqual(result[1], '{  }')
        self.assertEqual(result[2], ' abc')

    def test_should_throw_on_unexpected_end_of_quoted_key_or_string(self):
        with self.assertRaises(IndexError):
            to_string('{"}')

    def test_should_cope_with_all_kinds_of_whitespace(self):
        input = ' {  \t "test"\t: \t 123 \r \n }'
        result = to_string(input)
        expected = '{ "test": 123 }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_when_changing_single_quoted_string_to_double_quotes_needs_to_quote_double_quotes(self):
        input = """{ 'abc "': 'test' }"""
        result = to_string(input)
        expected = '{ "abc \\"": "test" }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_when_changing_single_quoted_string_to_double_quotes_needs_to_unquote_single_quotes(self):
        with open('./singlequoted.txt', 'r') as file:
            input = file.read()
        result = to_string(input)
        expected = """{ "abc '": "test'", "key": 123 }"""
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_when_changing_backtick_quoted_string_to_double_quotes_needs_to_fix_quotes(self):
        input = "{ `abc \'\"`: `test\'\"`, 'key': 123}"
        result = to_string(input)
        expected = """{ "abc '\\"": "test'\\"", "key": 123 }"""
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_when_changing_backticked_quoted_string_to_double_quotes_needs_to_unquote_single_quotes_but_not_double(self):
        with open('./backticked.txt', 'r') as file:
            input = file.read()
        result = to_string(input)
        expected = """{ "abc '\\"`": "test`'\\"", "key": 123 }"""
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_cope_with_trailing_comma_in_key_value_pairs_for_object(self):
        input = '{ "abc": 123, }'
        result = to_string(input)
        expected = '{ "abc": 123 }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_cope_with_circular_references(self):
        scenario = """{
    abc: <ref *1> {
        abc: 123,
        def: 'test',
        ghi: { jkl: 'test' },
        xyz: { zzz: 123, jj: 'test', abc: [Circular *1] }
    },
    def: <ref *2> {
        zzz: 123,
        jj: 'test',
        abc: <ref *1> {
        abc: 123,
        def: 'test',
        ghi: { jkl: 'test' },
        xyz: [Circular *2]
        }
    }
    }"""
        result = to_string(scenario)
        self.assertIn('"Circular"', result)
        self.assertTrue(self.assert_is_json(result))

    def test_can_cope_with_stringified_strings(self):
        scenario = '{\n  \"abc\": 123\n  }\n}'
        result = to_string(scenario)
        expected = '{ "abc": 123 }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_empty_object_is_valid_json(self):
        scenario = '{}'
        result = to_string(scenario)
        self.assertTrue(self.assert_is_json(result))

    def test_should_play_nice_with_empty_objects(self):
        scenario = '{ "t": [], "a": {} }'
        result = to_string(scenario)
        expected = '{ "t": [], "a": {  } }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_overly_stringified_objects(self):
        object = {
            'arr"ay': [
                1,
                {
                    'obj"ec\'}t': { "\n\nk\"\'ey": "\"\"''',value" },
                },
                [],
                {},
                True,
                None,
            ],
        }
        scenario = json.dumps(json.dumps(json.dumps(json.dumps(object))))
        result = to_string(scenario)
        self.assertTrue(self.assert_is_json(result))

    def test_should_concatenate_strings_with_plus(self):
        obj = '{ "abc": "test" + "test2" }'
        result = to_string(obj)
        expected = '{ "abc": "testtest2" }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_concatenate_strings_with_plus_and_preserve_whitespace(self):
        obj = '{ "abc": "test" + "test2" + "test3" }'
        result = to_string(obj)
        expected = '{ "abc": "testtest2test3" }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_concatenate_strings_with_different_quotes(self):
        obj = '{ "abc": \'test\' + `test2` + "test3" + \\"test4\\" }'
        result = to_string(obj)
        expected = '{ "abc": "testtest2test3test4" }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_python_true(self):
        obj = '{ "abc": True }'
        result = to_string(obj)
        expected = '{ "abc": true }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_python_false(self):
        input_object = '{ "abc": False }'
        result = to_string(input_object)
        expected = '{ "abc": false }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_change_none_primitive_to_null(self):
        input_object = '{ "abc": None }'
        result = to_string(input_object)
        expected = '{ "abc": null }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_change_noNe_primitive_to_null(self):
        input_object = "{'intent': {'slots': {'location': noNe}, 'confirmationState': 'None', 'name': 'JobSearch', 'state': 'InProgress'}, 'nluConfidence': 0.8}"
        result = to_string(input_object)
        expected = '{ "intent": { "slots": { "location": null }, "confirmationState": "None", "name": "JobSearch", "state": "InProgress" }, "nluConfidence": 0.8 }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_treat_space_in_key_name_as_terminator_if_no_in_quotes(self):
        input_object = " { toString } "
        with self.assertRaises(Exception, msg="Expected colon"):
            to_string(input_object)

    def test_should_support_null_key_name(self):
        input_object = " { [null]: 'test' } "
        result = to_string(input_object)
        self.assertTrue(self.assert_is_json(result))

    def test_bug_should_support_newline_after_object_before_array_end(self):
        input_object = """{
        savedJobs: [
            {
                external: false
            }
        ]
    }"""
        result = to_string(input_object)
        self.assertTrue(self.assert_is_json(result))

    def test_should_support_trailing_comma_in_array_1(self):
        input_object = """{
        savedJobs: [
            {
                external: false
            },
        ]
    }"""
        result = to_string(input_object)
        self.assertTrue(self.assert_is_json(result))

    def test_should_support_trailing_comma_in_array_2(self):
        input_object = "{ arr: [1,2,3,]}"
        result = to_string(input_object)
        expected = '{ "arr": [1, 2, 3] }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_support_trailing_comma_in_array_3(self):
        input_object = "{ arr: [,]}"
        result = to_string(input_object)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_escaped_double_quotes_used_as_quotes_aka_kibana(self):
        input_object = '{\\"@metadata\\":{\\"beat\\":\\"filebeat\\"}}'
        result = to_string(input_object)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_escaped_double_quotes_used_as_quotes_inside_strings(self):
        input_object = '{\\"@metadata\\":{\\"message\\":\\"{\\\\"url\\\\": \\\\"hey\\\\"}\\"}}'
        result = to_string(input_object)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_double_escaped_double_quotes_used_as_quotes_case_1(self):
        input_object = '{ \\\\"test\\\\": \\\\"test1\\\\" }'
        result = to_string(input_object)
        expected = '{ "test": "test1" }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_double_escaped_double_quotes_used_as_quotes_case_2(self):
        input_object = '{\\"@metadata\\":{\\"message\\":\\"{\\\\"url\\\\": \\\\"hey\\\\"}\\"}}'
        result = to_string(input_object)
        expected = '{ "@metadata": { "message": "{\\"url\\": \\"hey\\"}" } }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_pretty_formatted_sloping_double_quotes_as_output_by_word(self):
        input_object = '{\n"abc": “test”\n}'
        result = to_string(input_object)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_pretty_formatted_sloping_double_quotes_as_output_by_word_case_2(self):
        input_object = '{“abc”: “def”}'
        result = to_string(input_object)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_stack_overflow_json(self):
        input_object = '{\nstaus: "Success",\nid: 1,\ndata: [{\'Movie\':\'kung fu panda\',\'% viewed\': 50.5},{\'Movie\':\'kung fu panda 2\',\'% viewed\':1.5}],\nmetadata: {\'filters\':[\'Movie\', \'Percentage Viewed\' ] , \'params\':{\'content\':\'Comedy\', \'type\': \'Movie\'}}\n}'
        result = to_string(input_object)
        self.assertTrue(self.assert_is_json(result))

    def test_should_insert_missing_commas_between_key_value_pairs(self):
        input_object = '{\n"abc": "def"\n"ghi": "jkl"\n}'
        result = to_string(input_object)
        expected = '{ "abc": "def", "ghi": "jkl" }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_insert_missing_commas_between_key_value_pairs_case_2(self):
        input_object = '{\n"abc": "def"\n"ghi": "jkl"\n"mno": "pqr"\n}'
        result = to_string(input_object)
        expected = '{ "abc": "def", "ghi": "jkl", "mno": "pqr" }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_insert_missing_commas_between_array_elements(self):
        input_object = '{\n"abc": [\n"def"\n"ghi" 3 true null\n]\n}'
        result = to_string(input_object)
        expected = '{ "abc": ["def", "ghi", 3, true, null] }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))

    def test_should_error_the_right_way_given_broken_json(self):
        input_object = '{ "test": "bad  { "test": "good" }'
        with self.assertRaises(Exception, msg="Expected colon"):
            to_string(input_object)

    def test_should_cope_with_a_difficult_scenario(self):
        input_object = '{ \nvalue: true peter: \'fun\' number: 3 somekey: "a string"\narray: [ 2 9234 98234 9 9213840  98213409 98234]\n}'
        result = to_string(input_object)
        self.assertTrue(self.assert_is_json(result))

    def test_should_cope_with_unquoted_single_quote_inside_single_quoted_string_if_an_s_follows(self):
        input_object = "{ 'test': 'test's' }"
        result = to_string(input_object)
        expected = '{ "test": "test\'s" }'
        self.assertEqual(result, expected)
        self.assertTrue(self.assert_is_json(result))


if __name__ == '__main__':
    unittest.main()

