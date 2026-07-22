export interface ICheckboxOptionBase {
  label: string;
  value: string;
  defaultChecked?: boolean;
}

export interface ICheckboxOptionWithIcon extends ICheckboxOptionBase {
  icon: string;
}

export interface ICheckboxOptionWithoutIcon extends ICheckboxOptionBase {
  icon?: never;
}

export type CheckboxOption =
  | ICheckboxOptionWithIcon
  | ICheckboxOptionWithoutIcon;

type ValueTuple<T extends readonly CheckboxOption[]> = {
  [K in keyof T]: T[K] extends { value: infer V extends string } ? V : never;
};

type HasDuplicateValues<
  T extends readonly string[],
  Seen extends string = never,
> = T extends readonly [
  infer Head extends string,
  ...infer Tail extends string[],
]
  ? Head extends Seen
    ? true
    : HasDuplicateValues<Tail, Seen | Head>
  : false;

type IsUniformIconUsage<T extends readonly CheckboxOption[]> =
  T extends readonly [
    infer Head extends CheckboxOption,
    ...infer Tail extends readonly CheckboxOption[],
  ]
    ? Head extends ICheckboxOptionWithIcon
      ? Tail[number] extends ICheckboxOptionWithIcon
        ? true
        : false
      : Tail[number] extends ICheckboxOptionWithoutIcon
        ? true
        : false
    : true;

export type ValidateCheckboxOptions<T extends readonly CheckboxOption[]> =
  IsUniformIconUsage<T> extends true
    ? HasDuplicateValues<ValueTuple<T>> extends true
      ? never
      : T
    : never;

export interface ICheckboxProps<T extends readonly CheckboxOption[]> {
  options: ValidateCheckboxOptions<T>;
  required?: boolean;
  onChange?: (value: string) => void;
}
