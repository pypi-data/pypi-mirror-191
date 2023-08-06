import { JupyterFrontEnd } from '@jupyterlab/application';
import { LabIcon } from '@jupyterlab/ui-components';
import { ICodeMirror } from '@jupyterlab/codemirror';
import { StringStream } from 'codemirror';

const FRED = {
  name: 'fred',
  displayName: 'FRED',
  extensions: ['fred', 'fredmod'],
  mimetype: 'application/x-fred',
  icon: new LabIcon({
    name: 'fredIcon',
    svgstr: `<svg xmlns="http://www.w3.org/2000/svg" width="320" height="320" viewBox="0 0 320 320">
      <g class="jp-icon-selectable">
        <path d="M225.3 143.6v32.8h-91.8v32.8H245V242H81v-98.4h144.3ZM81 110.8V78h157.4v32.8H81Z" fill="#FFF"/>
      </g>
    </svg>`
  })
};

const blocks = [
  'agent_restart',
  'agent_startup',
  'comment',
  'condition',
  'configuration',
  'group_restart',
  'group_startup',
  'network',
  'place',
  'prototype',
  'restart',
  'simulation',
  'startup',
  'state',
  'use',
  'variables'
];

// place blocks have dynamic property names ex. contact_prob_for<condition_name>
// use/prototype blocks are completely dynamic (https://docs.epistemix.com/projects/lang-guide/en/latest/chapter14.html) so maybe it makes sense to look at patterns instead of keywords?
const properties = [
  'all_group_agents',
  'condition_timing',
  'contact_prob',
  'contact_rate',
  'country',
  'days',
  'default_model',
  'dump_files',
  'enable_agent_records',
  'enable_aging',
  'enable_population_dynamics',
  'enable_transmission_bias',
  'end_date',
  'exposed_state',
  'file_buffer_size',
  'group_start_state',
  'has_group_agent',
  'is_directed',
  'locations',
  'max_loops',
  'meta_start_state',
  'output',
  'output_interval',
  'population_directory',
  'population_version',
  'same_age_bias',
  'seed',
  'shuffle',
  'snapshot_date',
  'snapshot_final',
  'snapshot_interval',
  'snapshots',
  'start_date',
  'start_state',
  'substeps',
  'test',
  'transmissibility',
  'transmission_mode', // both?
  'transmission_model', // both?
  'transmission_network_name',
  'update_progress',
  'use_index_id',
  'use_mean_latitude',
  'weekly_data'
];

const keywords = [
  'agent',
  'do',
  'else',
  'for',
  'if',
  'include',
  'list',
  'list_table',
  'numeric',
  'shared',
  'table',
  'then',
  'with'
];

// const variables = [ // constants?
//   'Excluded', // ?
//   'today'
// ];

const functions = [
  'abs',
  'acos',
  'acosh',
  'add',
  'apply',
  'arg_sort',
  'asin',
  'asinh',
  'ask',
  'atan',
  'atan2',
  'atanh',
  'bernoulli',
  'binomial',
  'cauchy',
  'ceil',
  'chi_squared',
  'cos',
  'cosh',
  'current_place',
  'current_count',
  'current_state',
  'daily_count',
  'dist',
  'distance',
  'div',
  'elevation',
  'equal',
  'exp',
  'exponential',
  'extreme_value',
  'filter_agents',
  'filter_by_index',
  'filter_values',
  'find_index',
  'fisher_f',
  'floor',
  'foreach_get',
  'gamma',
  'geometric',
  'get_active_places_just_opening',
  'get_contact_rate',
  'get_container',
  'get_day_from_timestamp',
  'get_group_agent',
  'get_group_agents',
  'get_group_id',
  'get_hour_from_timestamp',
  'get_keys',
  'get_month_from_timestamp',
  'get_next_open_period',
  'get_number_of_transmissibles',
  'get_open_period',
  'get_population',
  'get_role',
  'get_same_age_bias',
  'size',
  'get_size',
  'get_transmissibility',
  'get_transmissible_list',
  'get_values',
  'get_year_from_timestamp',
  'getx',
  'gety',
  'gompertz',
  'index_agents',
  'index_values',
  'inlinks',
  'int',
  'intersection',
  'last',
  'latitude',
  'length',
  'links',
  'list',
  'log',
  'lognormal',
  'longitude',
  'lookup',
  'lookup_list',
  'lookup_list_table_value',
  'max',
  'members',
  'min',
  'mod',
  'mult',
  'negative_binomial',
  'normal',
  'nprob',
  'outlinks',
  'partial_sums',
  'percentile',
  'poisson',
  'pow',
  'prev_state',
  'prod',
  'range',
  'range_list',
  'read',
  'read_agent_file',
  'read_group_file',
  'read_place_file',
  'round',
  'sample_with_replacement',
  'sample_without_replacement',
  'select',
  'select_index',
  'set_difference',
  'shuffle',
  'sim_step',
  'sin',
  'sinh',
  'sort',
  'source',
  'sqrt',
  'steps_between',
  'student_t',
  'sub',
  'sum',
  'sus_list',
  'sus_list',
  'tan',
  'tanh',
  'total_count',
  'transmissions',
  'uniform',
  'union',
  'unique',
  'until',
  'weibull',
  'now',
  'sim_day',
  'sim_run',
  'day_of_week',
  'day_of_month',
  'day_of_year',
  'month',
  'year',
  'today',
  'date',
  'hour',
  'epi_week',
  'epi_year',
  'id',
  'birth_year',
  'age_in_days',
  'age_in_years',
  'real_age',
  'age',
  'eq',
  'neq',
  'lt',
  'lte',
  'gt',
  'gte',
  'is_in_list',
  'is_in_range',
  'is_date_in_range',
  'is_file_open',
  'is_restart',
  'is_member',
  'is_meta_agent',
  'is_group_agent',
  'is_open',
  'is_group_open',
  'was_exposed_in',
  'was_exposed_externally',
  'is_temporarily_closed',
  'is_connected_to',
  'is_connected_from',
  'is_at',
  'is_skipping',
  'abort',
  'add_edge',
  'delete_edge',
  'set_weight',
  'get_weight',
  'shortest_path',
  'edge_neighborhood',
  'weight_neighborhood',
  'add_edge_from',
  'add_edge_to',
  'add_site',
  'add_to_schedule',
  'adjust_contacts',
  'attend',
  'clear',
  'clear_schedule',
  'clear_transmissible_agents',
  'close',
  'delete_edge_from',
  'delete_edge_to',
  'die',
  'exit',
  'erase',
  'give_birth',
  'activate_agent',
  'set_age',
  'assign_agent_to_place',
  'assign_agent_to_network',
  'new_agent',
  'import_exposures',
  'join',
  'move',
  'move_to',
  'move_to_location',
  'open_csv',
  'pop',
  'preferential_attachment_network',
  'print',
  'print_csv',
  'print_file',
  'print_event_file',
  'print_event',
  'push',
  'quit',
  'randomize_network',
  'read_container_file',
  'read_list_table',
  'read_schedule_file',
  'read_table',
  'remove_from_schedule',
  'reopen',
  'reset_schedule',
  'send',
  'set',
  'set_state',
  'set_sus',
  'set_trans',
  'set_weight_from',
  'set_weight_to',
  'get_weight_from',
  'get_weight_to',
  'skip',
  'tell',
  'transmit',
  'wait',
  // Custom
  'default',
  'next',
  'prob',
  'not'
];

const operators = ['-', '+', '/', '*', '=', '<', '>', '!', '&', '=='];

const tokenRegex = /[A-Za-z0-9\-_#]+/;
const charRegex = /[{}().,]/; // Special characters that should return as a token but should stop regex search

function registerFREDFileType(app: JupyterFrontEnd) {
  app.docRegistry.addFileType({
    name: FRED.name,
    displayName: FRED.displayName,
    extensions: FRED.extensions.map(m => `.${m}`),
    mimeTypes: [FRED.mimetype],
    icon: FRED.icon,
    iconLabel: FRED.displayName
  });
}

function registerFREDWithCodeMirror(codeMirror: ICodeMirror['CodeMirror']) {
  codeMirror.defineMode(FRED.name, () => {
    return {
      startState() {
        return {
          previousToken: null,
          currentToken: null,
          nextToken: null,
          mode: false
        };
      },
      token: (stream, state) => {
        // update indentation, but only if indentStack is empty
        // if (state.indentStack === null && stream.sol()) {
        //   state.indentation = stream.indentation();
        // }
        // skip spaces
        if (stream.eatSpace()) {
          return null;
        }
        let returnType = null;
        const ch = stream.next();
        let isFunction = false;
        let isObjProp = false;
        switch (state.mode) {
          case 'comment':
            returnType = 'comment';
            if (ch === '}') {
              state.mode = false;
            }
            break;
          case 'string':
            returnType = 'string';
            if (ch === '"') {
              state.mode = false;
            }
            break;
          default:
            console.log('ch: ', ch);
            if (ch && charRegex.test(ch)) {
              stream.eatWhile(charRegex);
            } else if (ch && tokenRegex.test(ch)) {
              stream.eatWhile(tokenRegex);
            }
            state.currentToken = stream.current();
            state.nextToken = getNextToken(stream);
            isFunction = state.nextToken === '(';
            isObjProp = state.previousToken === '.';
            console.log('current: ', '|' + state.currentToken + '|');
            console.log('previous: ', state.previousToken);
            console.log('next: ', state.nextToken);

            // Block
            if (
              blocks.includes(state.currentToken) &&
              /[{\w]/.test(state.nextToken)
            ) {
              if (state.currentToken === 'comment') {
                state.mode = 'comment';
                returnType = 'comment';
              } else {
                returnType = 'block';
              }
            }
            // Property
            else if (
              properties.includes(state.currentToken) &&
              !isObjProp &&
              state.nextToken === '='
            ) {
              returnType = 'property';
            }
            // Function
            else if (functions.includes(state.currentToken) && isFunction) {
              returnType = 'function';
            }
            // Keyword
            else if (keywords.includes(state.currentToken)) {
              returnType = 'keyword';
            }
            // Singleline comment
            else if (state.currentToken.startsWith('#')) {
              returnType = 'comment';
              stream.skipToEnd();
            }
            // String
            else if (state.currentToken.startsWith('"')) {
              returnType = 'string';
              state.mode = 'string';
            }
            // Operator
            else if (operators.includes(state.currentToken)) {
              returnType = 'operator';
            }
            // Number
            else if (/^-?\d+$/.test(state.currentToken)) {
              returnType = 'number';
            }
        }
        state.previousToken = state.currentToken;
        return returnType ? `fred-${returnType}` : returnType;
      },

      // indent: state => {
      //   if (state.indentStack === null) {
      //     return state.indentation;
      //   }
      //   return state.indentStack.indent;
      // },

      lineComment: '#'
    };
  });

  codeMirror.defineMIME(FRED.mimetype, FRED.name);

  codeMirror.modeInfo.push({
    name: FRED.displayName,
    mime: FRED.mimetype,
    mode: FRED.name,
    ext: FRED.extensions
  });
}

function getNextToken(stream: StringStream) {
  let output = null;
  let lineNumber = 1;
  let line: string | undefined = '';

  stream.eatSpace();
  if (stream.eol()) {
    while (output === null) {
      line = stream.lookAhead(lineNumber);
      if (line === undefined) {
        break;
      }
      const charMatches = line.match(charRegex);
      const tokenMatches = line.match(tokenRegex);
      if (charMatches) {
        output = charMatches[0].trim();
      }
      if (tokenMatches) {
        output = tokenMatches[0].trim();
      }
      lineNumber++;
    }
  } else {
    // console.log(stream, stream.current());
    const charMatches = stream.match(charRegex, false);
    const tokenMatches = stream.match(tokenRegex, false);
    if (charMatches) {
      output = charMatches[0].trim();
    }
    if (tokenMatches) {
      output = tokenMatches[0].trim();
    }
    if (output === null) {
      output = stream.peek();
    }
  }
  return output;
}

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export function registerFRED(
  app: JupyterFrontEnd,
  codeMirror: ICodeMirror['CodeMirror']
): void {
  registerFREDFileType(app);
  registerFREDWithCodeMirror(codeMirror);
}
