#include <stdio.h>
#include <string.h>
#include <unistd.h>

struct flags {
  unsigned long a: 42;
  unsigned int b: 7;
};

int main(void) {
  struct flags my_flags;
  unsigned char buffer[1000];

  /* Set a to all 1s. */
  my_flags.a = 4398046511103U;
  memcpy(buffer, &my_flags, sizeof(my_flags));
  write(1, buffer, sizeof(my_flags));
  my_flags.a = 0;

  /* Set b to all 1s. */
  my_flags.b = 127U;
  memcpy(buffer, &my_flags, sizeof(my_flags));
  write(1, buffer, sizeof(my_flags));
  my_flags.b = 0;

  return 0;
}
